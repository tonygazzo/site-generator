class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"[HTMLNode - tag: {self.tag}; value: {self.value}; children: {self.children}; props: {self.props}]"

    def to_html(self):
        raise NotImplementedError("Subclasses must implement this method")

    def props_to_html(self):
        s = ""
        for k, v in self.props.items():
            s += f' {k}="{v}"'
        return s
