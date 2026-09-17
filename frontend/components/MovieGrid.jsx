import MovieCard from "./MovieCard";

export default function MovieGrid({ movies }) {
  if (!movies || movies.length === 0) {
    return null;
  }

  return (
    <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-5">
      {movies.map((movie) => (
        <MovieCard
          key={movie.movie_id}
          movie={movie}
        />
      ))}
    </div>
  );
}