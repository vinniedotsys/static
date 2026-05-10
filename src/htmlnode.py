

class HtmlNode():
    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        astr = ""
        if self.props:
            for key in self.props:
                astr += ' ' + key + '="' + self.props[key] + '"'
        return astr


    def __repr__(self) -> str:
        props = self.props_to_html()
        return f"HtmlNode({self.tag}, {self.value}, {self.children}, {props})"

class LeafNode(HtmlNode):
    def __init__(self, tag=None, value=None, props=None) -> None:
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return str(self.value)
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        props = self.props_to_html()
        return f"HtmlNode({self.tag}, {self.value}, {props})"

class ParentNode(HtmlNode):
