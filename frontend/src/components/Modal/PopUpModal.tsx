import { useEffect, useRef } from "react";
import { type ModalSizeVariants, modalSizeVariants } from "./config";
import { CloseButton } from "../Button";
import clsx from "clsx";





type ModalProps = {
    variant?: ModalSizeVariants;
    setShowModal: (visible: boolean) => void;
    children: React.ReactNode;
    className?: string;
};

export default function Modal({
    variant = "default", // default applied here
    setShowModal,
    children,
    className,
}: ModalProps) {
    const modalRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (
                modalRef.current &&
                !modalRef.current.contains(event.target as Node)
            ) {
                setShowModal(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, [setShowModal]);
    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center  bg-opacity-50 border-2 ">
            <div
                ref={modalRef}
                className={clsx(
                    "flex flex-col bg-white  border-gray-300 rounded-lg shadow-xl/30 p-8 overflow-auto dark:bg-background",
                    modalSizeVariants[variant],
                    className
                )}
            >
                <div className="self-end">
                    {" "}
                    <CloseButton onClick={() => setShowModal(false)} />
                </div>
                {children}
            </div>
        </div>
    );
}
