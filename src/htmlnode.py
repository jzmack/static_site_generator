class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if not self.props:
            return ""
        formatted_string = ""
        for key, value in self.props.items():
            attrib_string = f' {key}="{value}"'
            formatted_string += attrib_string
        return formatted_string

    def __repr__(self):
        return f"HTMLNode({self.tag!r}, {self.value!r}, {self.children!r}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("LeafNode must have a value.")
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        
        if self.tag is None:
            return self.value
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("ParentNode requires a non-None tag.")
        if children is None:
            raise ValueError("ParentNode requires a non-None children list.")
        if not isinstance(children, list):
            raise TypeError("children must be a list.")
        for child in children:
            if not isinstance(child, HTMLNode):
                raise TypeError("All children must be instances of HTMLNode.")
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Cannot render HTML without a tag.")
        if self.children is None:
            raise ValueError("Cannot render HTML without children.")
        
        children_html = ""
        for child in self.children:
            if not hasattr(child, "to_html") or not callable(child.to_html):
                raise TypeError("Each child must have a callable to_html() method.")
            children_html += child.to_html()
        
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

