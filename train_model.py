from torch.utils.data import Dataset
from tokenizers import ByteLevelBPETokenizer
from tokenizers.processors import BertProcessing
from transformers import Trainer
from pathlib import Path

class SchlagerDataset(Dataset):
    def __init__(self, evaluate: bool = False):
        tokenizer = ByteLevelBPETokenizer(
            "./model/schlager_bot-vocab.json",
            "./model/schlager_bot-merges.txt",
        )
        tokenizer._tokenizer.post_processor = BertProcessing(
            ("</s>", tokenizer.token_to_id("</s>")),
            ("<s>", tokenizer.token_to_id("<s>")),
        )
        tokenizer.enable_truncation(max_length=512)
        # or use the RobertaTokenizer from `transformers` directly.

        self.examples = []

        src_files = Path("./training_data/").glob("*-eval.txt") if evaluate else Path("./training_data/").glob("*-train.txt")
        for src_file in src_files:
            print("🔥", src_file)
            lines = src_file.read_text(encoding="utf-8").splitlines()
            self.examples += [x.ids for x in tokenizer.encode_batch(lines)]

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        # We’ll pad at the batch level.
        return torch.tensor(self.examples[i])
    
if __name__ == "__main__":

    sub_dataset = SchlagerDataset(Dataset)
    length = sub_dataset.__len__

    print(length)

    # trainer = Trainer(
    #         model = None
    #         output_dir = "./model/EsperBERTo-small-v1",
    #         model_type= "roberta",
    #         "mlm",
    #         config_name = "./models/EsperBERTo-small",
    #         tokenizer_name = "./models/EsperBERTo-small",
    #         "do_train",
    #         "do_eval",
    #         learning_rate = "1e-4"
    #         --num_train_epochs 5
    #         --save_total_limit 2
    #         --save_steps 2000
    #         --per_gpu_train_batch_size 16
    #         --evaluate_during_training
    #         --seed 42
    # )