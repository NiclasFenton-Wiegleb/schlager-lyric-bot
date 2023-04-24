import transformers
import json
from tokenizers import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing
import datasets
import os
from tokenizers import BertWordPieceTokenizer
from itertools import chain
from transformers import DataCollatorForLanguageModeling
from transformers import TrainingArguments
from transformers import Trainer



def group_texts(examples):
    # Concatenate all texts.
    concatenated_examples = {k: list(chain(*examples[k])) for k in examples.keys()}
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # We drop the small remainder, we could add padding if the model supported it instead of this drop, you can
    # customize this part to your needs.
    if total_length >= max_length:
        total_length = (total_length // max_length) * max_length
    # Split by chunks of max_len.
    result = {
        k: [t[i : i + max_length] for i in range(0, total_length, max_length)]
        for k, t in concatenated_examples.items()
    }
    return result
# #Loading the lyrics data as the dataset

# #Iterating through the files in the directory and adding the names to the files variable

# files = []

# directory = "./lyrics"

# for filename in os.scandir(directory):
#     if filename.is_file():
#         files.append(filename.path)

# dataset = datasets.load_dataset("text", data_files= files, split= "train")

# d = dataset.train_test_split(test_size= 0.1)
# d["train"], d["test"]

# def dataset_to_text(dataset, output_filename="data.txt"):
#   """Utility function to save dataset text to disk,
#   useful for using the texts to train the tokenizer 
#   (as the tokenizer accepts files)"""
#   with open(output_filename, "w") as f:
#     for t in dataset["text"]:
#       print(t, file=f)

# # save the training set to train.txt
# dataset_to_text(d["train"], "./model/model_data/train.txt")
# # save the testing set to test.txt
# dataset_to_text(d["test"], "./model/model_data/test.txt")

# special_tokens = [
#   "[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]", "<S>", "<T>"
# ]

# training_file = ["./model/model_data/train.txt"]
# # 30,522 vocab is BERT's default vocab size
vocab_size = 30_522
# # maximum sequence length, lowering will result to faster training (when increasing batch size)
max_length = 512
# # whether to truncate
# truncate_longer_samples = False

# #Initialize the WordPiece tokenizer
# tokenizer = BertWordPieceTokenizer()

# #Train the tokenizer
# tokenizer.train(files=training_file, vocab_size=vocab_size, special_tokens=special_tokens)

# # #Enable truncation up to the maximum 512 tokens
# # tokenizer.enable_truncation(max_length=max_length)

model_path = "./model/tokenizer/"

d_train = datasets.load_dataset("text", data_files="./model/model_data/train.txt", split= "train")
d_test = datasets.load_dataset("text", data_files="./model/model_data/test.txt", split= "train")

#Save the tokenizer to directory
# tokenizer.save_model(model_path)

# #Dumping some of the tokenizer config to config file, 
# #including special tokens, whether to lower case and the maximum sequence length
# with open(os.path.join(model_path, "config.json"), "w") as f:
#   tokenizer_cfg = {
#       "do_lower_case": True,
#       "unk_token": "[UNK]",
#       "sep_token": "[SEP]",
#       "pad_token": "[PAD]",
#       "cls_token": "[CLS]",
#       "mask_token": "[MASK]",
#       "model_max_length": max_length,
#       "max_len": max_length,
#   }
#   json.dump(tokenizer_cfg, f)

  #Let's load the tokenizer
tokenizer = transformers.BertTokenizerFast.from_pretrained(model_path)

#Tokenizing the training dataset
train_dataset = d_train.map((lambda x: tokenizer(x["text"], return_special_tokens_mask=True)), batched= True)

#Tokenizing the test dataset
test_dataset = d_test.map((lambda x: tokenizer(x["text"], return_special_tokens_mask=True)), batched= True)

# remove other columns, and remain them as Python lists
test_dataset.set_format(columns=["input_ids", "attention_mask", "special_tokens_mask"])
train_dataset.set_format(columns=["input_ids", "attention_mask", "special_tokens_mask"])


train_dataset = train_dataset.map(group_texts, batched=True,
                                    desc=f"Grouping texts in chunks of {max_length}")
test_dataset = test_dataset.map(group_texts, batched=True,
                                desc=f"Grouping texts in chunks of {max_length}")

#Convert the datasets from lists to torch tensors
train_dataset.set_format("torch")
test_dataset.set_format("torch")


print(len(train_dataset), len(test_dataset))

# initialize the model with the config
model_config = transformers.BertConfig(vocab_size=vocab_size, max_position_embeddings=max_length)
model = transformers.BertForMaskedLM(config=model_config)

# initialize the data collator, randomly masking 20% (default is 15%) of the tokens for the Masked Language
# Modeling (MLM) task
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=True, mlm_probability=0.2
)

trained_model_path = "./model/trained_model"

training_args = TrainingArguments(
    output_dir=trained_model_path,          # output directory to where save model checkpoint
    evaluation_strategy="epoch",    # evaluate each `logging_steps` steps
    overwrite_output_dir=True,      
    num_train_epochs=10,            # number of training epochs, feel free to tweak
    per_device_train_batch_size=10, # the training batch size, put it as high as your GPU memory fits
    gradient_accumulation_steps=8,  # accumulating the gradients before updating the weights
    per_device_eval_batch_size=64,  # evaluation batch size
    logging_steps=1000,             # evaluate, log and save model checkpoints every 1000 step
    save_steps=1000,
    # load_best_model_at_end=True,  # whether to load the best model (in terms of loss) at the end of training
    # save_total_limit=3,           # whether you don't have much space so you let only 3 model weights saved in the disk
)

# initialize the trainer and pass everything to it
trainer = Trainer(
    model=model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# train the model
trainer.train()