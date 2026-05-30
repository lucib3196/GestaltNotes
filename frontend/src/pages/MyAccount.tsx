import { AccountHeader, AccountProfile } from "../features/Auth"

export default function MyAccount() {
    return <div className="flex flex-col gap-10 w-full items-center justify-center h-full "><AccountHeader /><AccountProfile /></div>
}