"use client";

import { useState } from "react";

export default function MovieSearch({
  movies,
  onRecommend,
  loading
}) {

  const [search, setSearch] = useState("");

  const filteredMovies = movies
    .filter((movie) =>
      movie.toLowerCase().includes(
        search.toLowerCase()
      )
    )
    .slice(0, 10);

  const handleSubmit = (event) => {

    event.preventDefault();

    if (!search.trim()) {
      return;
    }

    onRecommend(search);
  };

  return (
    <div className="mb-12">

      <h2 className="text-2xl font-extrabold">
        What do you want to watch?
      </h2>

      <p className="mt-2 text-sm text-gray-500">
        Search for a movie and discover similar titles.
      </p>

      <form
        onSubmit={handleSubmit}
        className="mt-5 flex flex-col gap-3 md:flex-row"
      >

        <div className="relative flex-1">

          <input
            type="text"
            value={search}
            onChange={(e) =>
              setSearch(e.target.value)
            }
            placeholder="Search movies..."
            className="w-full rounded-xl border border-white/10 bg-[#151922] px-5 py-4 text-white outline-none transition focus:border-red-500"
          />

          {search && filteredMovies.length > 0 && (

            <div className="absolute left-0 right-0 top-full z-50 mt-2 max-h-60 overflow-auto rounded-xl border border-white/10 bg-[#171a21] shadow-2xl">

              {filteredMovies.map((movie) => (

                <button
                  key={movie}
                  type="button"
                  onClick={() => {
                    setSearch(movie);
                  }}
                  className="block w-full px-5 py-3 text-left text-sm text-gray-300 transition hover:bg-white/10 hover:text-white"
                >
                  {movie}
                </button>

              ))}

            </div>

          )}

        </div>

        <button
          type="submit"
          disabled={loading}
          className="rounded-xl bg-red-600 px-8 py-4 font-bold transition hover:bg-red-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading
            ? "Finding..."
            : "✨ Recommend"}
        </button>

      </form>

    </div>
  );
}