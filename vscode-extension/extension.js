const vscode = require("vscode");

function activate(context) {

    const keywords = [
        "agar",
        "warna",
        "nahi",
        "jabtak",
        "dohrav",
        "ant",
        "bata",
        "likha",
        "bol",
        "aur",
        "ya"
    ];

    const completionProvider = vscode.languages.registerCompletionItemProvider(
        "bhojlang",
        {
            provideCompletionItems() {
                return keywords.map(word => {
                    const item = new vscode.CompletionItem(
                        word,
                        vscode.CompletionItemKind.Keyword
                    );

                    item.insertText = word;
                    item.detail = "BhojLang keyword";

                    return item;
                });
            }
        }
    );

    const runCommand = vscode.commands.registerCommand(
        "bhojlang.runFile",
        () => {
            const editor = vscode.window.activeTextEditor;

            if (!editor) {
                vscode.window.showErrorMessage("No BhojLang file is open.");
                return;
            }

            const filePath = editor.document.fileName;

            if (!filePath.endsWith(".bhoj")) {
                vscode.window.showErrorMessage(
                    "Please open a .bhoj file."
                );
                return;
            }

            const terminal = vscode.window.createTerminal("BhojLang");
            terminal.show();

            terminal.sendText(
                `python3 "$HOME/bhojlang/bhojlang.py" "${filePath}"`
            );
        }
    );

    context.subscriptions.push(
        completionProvider,
        runCommand
    );
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
