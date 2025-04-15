class StepsDenoise:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "steps": ("INT", {
                    "default": 24,
                    "min": 1,
                    "max": 64,
                    "step": 1,
                    "display": "slider"
                }),
                "denoise": ("FLOAT", {
                    "default": 0.6,
                    "min": 0,
                    "max": 1,
                    "step": 0.01,
                    "display": "number"
                }),
            },
        }

    RETURN_TYPES = ("INT","INT","FLOAT")
    RETURN_NAMES = ("steps","start at step","denoise")

    FUNCTION = "calculate"

    #OUTPUT_NODE = False

    CATEGORY = "SelectiveD"

    def calculate(self, steps, denoise):
        if denoise >= 1:
            start_at_step = 0
        elif denoise <= 0:
            start_at_step = 1
            steps = 1
        else:
            start_at_step = round((steps / denoise) * (1 - denoise))
            steps = steps + start_at_step

        print(f"""stepsDenoise:
                steps: {steps}
                start_at_step: {start_at_step}
            """)

        return (steps,start_at_step,denoise,)


NODE_CLASS_MAPPINGS = {
    "StepsDenoise": StepsDenoise
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StepsDenoise": "Steps Denoise"
}
