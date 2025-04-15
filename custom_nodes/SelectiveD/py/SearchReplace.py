class SearchReplace:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_text": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "search_text": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
                "replace_text": ("STRING", {
                    "multiline": True,
                    "default": ""
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output_text",)

    FUNCTION = "replace"

    #OUTPUT_NODE = False

    CATEGORY = "SelectiveD"

    def replace(self, input_text, search_text, replace_text):

        search_values = search_text.split("/")

        replace_values = replace_text.split("/")

        if len(search_values) != len(replace_values):
            raise Exception("Number of search texts have to match the number of replace texts")
        
        output_text = input_text
        
        for i in range(len(search_values)):
            output_text = output_text.replace(search_values[i], replace_values[i])

        print(f"""replace:
                output_text: {output_text}
            """)

        return (output_text,)


NODE_CLASS_MAPPINGS = {
    "SearchReplace": SearchReplace
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SearchReplace": "Search Replace"
}
