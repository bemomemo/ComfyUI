class NormalizeStartStop:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "denoise": ("FLOAT", {
                    "default": 0.6,
                    "min": 0,
                    "max": 1,
                    "step": 0.01,
                    "display": "number"
                }),
                "start_percent": ("FLOAT", {
                    "default": 0.0,
                    "min": 0,
                    "max": 1,
                    "step": 0.01,
                    "display": "number"
                }),
                "end_percent": ("FLOAT", {
                    "default": 1,
                    "min": 0,
                    "max": 1,
                    "step": 0.01,
                    "display": "number"
                }),
            },
        }

    RETURN_TYPES = ("FLOAT","FLOAT")
    RETURN_NAMES = ("start_percent","end_percent")

    FUNCTION = "normalize"

    #OUTPUT_NODE = False

    CATEGORY = "SelectiveD"

    def normalize(self, denoise, start_percent, end_percent):
        if denoise < 1 and denoise > 0:
            start = 1 - denoise

            if start_percent > 0:
                start_percent = start + (denoise * start_percent)

            if end_percent > 0:
                end_percent = start + (denoise * end_percent)

            if start_percent >= 1:
                start_percent = 1

            if start_percent <= 0:
                start_percent = 0

            if end_percent >= 1:
                end_percent = 1

            if end_percent <= 0:
                end_percent = 0   

        print(f"""normalize:
                denoise: {denoise}
                start_percent: {start_percent}
                end_percent: {end_percent}
            """)

        return (start_percent,end_percent,)


NODE_CLASS_MAPPINGS = {
    "NormalizeStartStop": NormalizeStartStop
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NormalizeStartStop": "Normalize Start Stop"
}
