import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/react";
import { HiDotsHorizontal, HiOutlinePencil, HiOutlineTrash } from "react-icons/hi";

export type ThreadActionsMenuProps = {
  title: string;
  deleting: boolean;
  onRename: () => void;
  onDelete: () => void;
};

export default function ThreadActionsMenu({
  title: displayTitle, deleting, onRename, onDelete,
}: ThreadActionsMenuProps) {
  return (
      <Menu>
        <MenuButton
          aria-label={`Options for ${displayTitle}`}
          className="inline-flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-text-soft hover:bg-surface-muted hover:text-text focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent/60"
        >
          <HiDotsHorizontal aria-hidden="true" className="h-4 w-4" />
        </MenuButton>
        <MenuItems
          anchor="bottom end"
          portal
          className="z-40 w-44 rounded-lg border border-border/60 bg-surface-strong p-1.5 text-sm text-text shadow-lg outline-none [--anchor-gap:6px]"
        >
          <MenuItem disabled={deleting}>
            <button
              type="button"
              disabled={deleting}
              onClick={onRename}
              className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-left data-focus:bg-surface-muted disabled:cursor-not-allowed disabled:opacity-50"
            >
              <HiOutlinePencil
                aria-hidden="true"
                className="h-4 w-4 text-text-soft"
              />
              Rename
            </button>
          </MenuItem>
          <div className="my-1 border-t border-border/40" />
          <MenuItem disabled={deleting}>
            <button
              type="button"
              disabled={deleting}
              onClick={onDelete}
              className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-left text-red-500 data-focus:bg-red-500/10 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <HiOutlineTrash aria-hidden="true" className="h-4 w-4" />
              {deleting ? "Deleting…" : "Delete"}
            </button>
          </MenuItem>
        </MenuItems>
      </Menu>
  );
}
