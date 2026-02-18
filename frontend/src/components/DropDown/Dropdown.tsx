import { useCallback } from "react";


export type DropDownBase = {
    selected: string;
    setSelected: (val: string) => void;
    label: string;
};

type DropDownProps = DropDownBase & {
    options: string[];
};
export default function DropDown({
    options,
    selected,
    setSelected,
    label = "Drop Down",
}: DropDownProps) {
    const handleDropDownChange = useCallback(
        (event: React.ChangeEvent<HTMLSelectElement>) => {
            setSelected(event.target.value);
        },
        [setSelected]
    );

    return (
        <div className="w-full flex flex-col gap-1">
            <label htmlFor="dropDown" className="text-sm font-medium text-slate-700">
                {label}
            </label>

            <select
                id="dropDown"
                name="dropDown"
                value={selected}
                onChange={handleDropDownChange}
                className="
          w-full rounded-md border border-slate-300 bg-white
          px-3 py-2 text-sm text-slate-800
          focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-violet-500
          hover:border-slate-400
        "
            >
                {options.map((v) => {
                    const cleaned = v.trim();
                    return (
                        <option key={cleaned} value={cleaned}>
                            {cleaned}
                        </option>
                    );
                })}
            </select>
        </div>
    );
}