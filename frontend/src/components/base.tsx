

export const BaseHtml = ({ children }: { children: undefined | {} }) => (
  <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Hello World</title>
      <script src="https://unpkg.com/htmx.org@1.9.6"></script>
      <script src="https://unpkg.com/htmx.org/dist/ext/sse.js"></script>
      <link href="https://cdn.jsdelivr.net/npm/daisyui@3.9.4/dist/full.css" rel="stylesheet" type="text/css" />
      <script src="https://cdn.tailwindcss.com"></script>
      <script>
        

      </script>
    </head>

    <body>
      <header >
        <nav class="navbar bg-base-300">
          <div class="flex-1">
            <a class="btn btn-ghost normal-case text-xl">Testing</a>
          </div>
          <div class="flex-none">
            <button class="btn btn-square btn-ghost">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="inline-block w-5 h-5 stroke-current"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z"></path></svg>
            </button>
          </div>
        </nav>
      </header>

      <main class="container mx-auto">
        {children}
      </main>
    </body>
  </html>
);
