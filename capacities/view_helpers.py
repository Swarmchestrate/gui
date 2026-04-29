from editor.view_helpers import EditorTableOfContents


class CloudCapacityEditorTableOfContents(EditorTableOfContents):
    disabled_categories = ["Edge Specific", "Networking"]


class EdgeCapacityEditorTableOfContents(EditorTableOfContents):
    disabled_categories = ["System Specific"]