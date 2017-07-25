import re


class TextProcessor:

    def remove_url(self, string):
        text = re.sub(r"http\S+", "", string)
        return text

    def remove_rt(self, string):
        text = re.sub(r"RT \S+", '', string)
        return text

    def remove_mentions(self, string):
        text = re.sub(r"@[^ ]+",'', string)
        return text

    def remove_newline(self, string):
        text = re.sub("\n", "", string)
        return text

    def clean(self, string):
        text = string
        text = self.remove_url(text)
        text = self.remove_rt(text)
        text = self.remove_mentions(text)
        text = self.remove_newline(text)

        return text.strip()
