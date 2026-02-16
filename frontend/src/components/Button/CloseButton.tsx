import { IoMdClose } from "react-icons/io";
import { useState } from "react";

type CloseButtonProps = {
    onClick: () => void
}

export function CloseButton({ onClick }: CloseButtonProps) {
    const [hover, setHover] = useState(false);

    return (
        <button
            onMouseEnter={() => setHover(true)}
            onMouseLeave={() => setHover(false)}
            className="transition-all duration-500"
            onClick={onClick}
            aria-label="Close"
        >
            <IoMdClose color={!hover ? "black" : "red"} size={30} />
        </button>
    );
}
