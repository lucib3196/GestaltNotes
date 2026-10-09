import { createPortal } from "react-dom";
import Modal from "../../../../components/Modal/Modal";
import type { Thread } from "../../../../services";
import RenameThreadForm from "./RenameThreadForm";

export type RenameThreadDialogProps = {
  thread: Thread;
  onClose: () => void;
  onRenamed: (thread: Thread) => void;
};

export default function RenameThreadDialog({
  thread, onClose, onRenamed,
}: RenameThreadDialogProps) {
  return createPortal(
    <Modal
      variant="small"
      presentation="modal"
      setShowModal={(visible) => {
        if (!visible) onClose();
      }}
    >
      <RenameThreadForm thread={thread} onClose={onClose} onRenamed={onRenamed} />
    </Modal>,
    document.body,
  );
}
