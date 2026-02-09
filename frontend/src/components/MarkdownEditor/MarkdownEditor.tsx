import React from "react";
import MDEditor from "@uiw/react-md-editor";

import { MathJax } from "better-react-mathjax";

export default function MarkDownEditor() {
    const [value, setValue] = React.useState<string | undefined>("");
    return (
        <MathJax>
            <MDEditor value={value} onChange={(val) => setValue(val)} />
        </MathJax>
    );
}
