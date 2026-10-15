import { AccountHeader, AccountProfile } from "./components";

export default function MyAccount() {
  return (
    <main className="mx-auto flex min-h-full w-full max-w-5xl flex-col gap-6 px-4 py-8 sm:px-6 lg:px-8">
      <AccountHeader />
      <AccountProfile />
    </main>
  );
}
