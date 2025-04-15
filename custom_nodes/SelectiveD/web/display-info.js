import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

// Displays input text on a node
app.registerExtension({
	name: "selectived.DisplayInfo",
	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		if (nodeData.name === "ImageInfo") {
			const onNodeCreated = nodeType.prototype.onNodeCreated;
				nodeType.prototype.onNodeCreated = function () {
					onNodeCreated ? onNodeCreated.apply(this, []) : undefined;
					this.showValueWidget = ComfyWidgets["STRING"](this, "output", ["STRING", { multiline: true }], app).widget;
					console.log(this.showValueWidget);
					this.showValueWidget.inputEl.readOnly = true;
					this.showValueWidget.inputEl.rows = 1;
				};

			const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted === null || onExecuted === void 0 ? void 0 : onExecuted.apply(this, [message]);
				this.showValueWidget.value = message.text.join("");
            };
		}
	},
});
