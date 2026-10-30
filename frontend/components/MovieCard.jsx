export default function MovieCard({ movie }) {
  return (
    <div className="movie-card group overflow-hidden rounded-xl border border-white/10 bg-[#14171e]">

      <div className="relative aspect-[2/3] overflow-hidden bg-[#1b1e25]">

        {movie.poster_url ? (
          <img
            src={movie.poster_url}
            alt={movie.title}
            className="poster h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-5xl text-gray-600">
            🎬
          </div>
        )}

        <div className="absolute left-3 top-3 rounded-md bg-black/75 px-2 py-1 text-xs font-bold text-red-400 backdrop-blur">
          {movie.match_percentage}% MATCH
        </div>

      </div>

      <div className="p-4">

        <h3 className="line-clamp-2 min-h-[48px] text-base font-bold text-white">
          {movie.title}
        </h3>

        <div className="mt-2 flex items-center gap-2 text-sm text-gray-400">

          <span className="font-bold text-yellow-400">
            ★ {movie.rating?.toFixed(1)}
          </span>

          <span>•</span>

          <span>
            {movie.release_year || "N/A"}
          </span>

        </div>

      </div>

    </div>
  );
}