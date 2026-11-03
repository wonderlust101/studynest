// Routes come from the file system: src/app/page.tsx is the "/" URL.
// Components here are Server Components by default, so they render on the server
// and ship no JavaScript to the browser. Add "use client" at the top of a file
// when a component needs state, effects or event handlers.
export default function HomePage() {
  return (
    <main className="flex flex-1 flex-col items-center justify-center gap-3 p-8 text-center">
      <h1 className="text-5xl font-bold tracking-tight">StudyNest</h1>
      <p className="text-lg opacity-70">
        Write notes, ask questions about them, and review what matters.
      </p>
    </main>
  );
}
