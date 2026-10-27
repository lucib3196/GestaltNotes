import clsx from "clsx";
import { useEffect, useRef } from "react";
import { CloseButton } from "../Button";
const modalSizeVariants = {
  small: "w-[min(92vw,28rem)] max-h-[82vh]",
  default: "w-[min(94vw,48rem)] max-h-[86vh]",
  large: "w-[min(96vw,72rem)] h-[min(88vh,52rem)]",
};

const modalPresentationVariants = {
  modal: {
    overlay:
      "fixed inset-0 z-50 flex items-center justify-center px-4 py-6 ",
    panel:
      "flex min-h-0 flex-col overflow-hidden rounded-lg border border-border bg-surface-strong text-text shadow-soft",
    ariaModal: true,
  },
  minimal: {
    overlay:
      "pointer-events-none fixed inset-0 z-50 flex items-start justify-end px-4 py-16",
    panel:
      "pointer-events-auto flex min-h-0 flex-col overflow-hidden rounded-lg border border-border bg-surface-strong text-text shadow-soft",
    ariaModal: false,
  },
};

type ModalSizeVariants = keyof typeof modalSizeVariants;
type ModalPresentationVariants = keyof typeof modalPresentationVariants;

type ModalProps = {
  variant?: ModalSizeVariants;
  presentation?: ModalPresentationVariants;
  setShowModal: (visible: boolean) => void;
  children: React.ReactNode;
  className?: string;
  contentClassName?: string;
};

export default function Modal({
  variant = "default",
  presentation = "modal",
  setShowModal,
  children,
  className,
  contentClassName,
}: ModalProps) {
  const modalRef = useRef<HTMLDivElement>(null);
  const presentationClasses = modalPresentationVariants[presentation];

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (
        modalRef.current &&
        !modalRef.current.contains(event.target as Node)
      ) {
        setShowModal(false);
      }
    }

    function handleEscape(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setShowModal(false);
      }
    }

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleEscape);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleEscape);
    };
  }, [setShowModal]);

  return (
    <div className={presentationClasses.overlay}>
      <div
        ref={modalRef}
        role="dialog"
        aria-modal={presentationClasses.ariaModal}
        className={clsx(
          presentationClasses.panel,
          modalSizeVariants[variant],
          className,
        )}
      >
        <div className="flex shrink-0 justify-end p-2">
          <CloseButton onClick={() => setShowModal(false)} />
        </div>
        <div
          className={clsx("min-h-0 flex-1 overflow-auto p-4", contentClassName)}
        >
          {children}
        </div>
      </div>
    </div>
  );
}
