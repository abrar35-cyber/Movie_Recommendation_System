"use client";

import { useEffect, useState } from "react";

import Hero from "../components/Hero";
import MovieSearch from "../components/MovieSearch";
import MovieGrid from "../components/MovieGrid";


const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";


export default function Home() {

  const [movies, setMovies] = useState([]);

  const [recommendations, setRecommendations] =
    useState([]);

  const [selectedMovie, setSelectedMovie] =
    useState("");

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");


  // ==========================================================
  // LOAD MOVIE LIST
  // ==========================================================

  useEffect(() => {

    async function loadMovies() {

      try {

        const response = await fetch(
          `${API_URL}/api/movies`
        );

        if (!response.ok) {
          throw new Error(
            "Failed to load movies"
          );
        }

        const data = await response.json();

        setMovies(data.movies);

      } catch (error) {

        console.error(error);

        setError(
          "Unable to connect to the movie server."
        );
      }
    }

    loadMovies();

  }, []);


  // ==========================================================
  // GET RECOMMENDATIONS
  // ==========================================================

  async function getRecommendations(title) {

    setLoading(true);

    setError("");

    try {

      const response = await fetch(
        `${API_URL}/api/recommend?title=${encodeURIComponent(title)}&limit=10`
      );

      if (!response.ok) {

        const errorData =
          await response.json();

        throw new Error(
          errorData.detail ||
          "Recommendation failed"
        );
      }

      const data =
        await response.json();

      setRecommendations(
        data.recommendations
      );

      setSelectedMovie(
        data.selected_movie
      );

      setTimeout(() => {

        document
          .getElementById("recommendations")
          ?.scrollIntoView({
            behavior: "smooth"
          });

      }, 100);

    } catch (error) {

      console.error(error);

      setError(
        error.message ||
        "Something went wrong."
      );

    } finally {

      setLoading(false);

    }
  }


  return (

    <main className="min-h-screen bg-[#0e1117] text-white">

      {/* ====================================================
          NAVBAR
      ==================================================== */}

      <nav className="sticky top-0 z-50 border-b border-white/10 bg-[#0e1117]/90 backdrop-blur-xl">

        <div className="mx-auto flex max-w-[1450px] items-center justify-between px-5 py-4 md:px-8">

          <div className="text-xl font-black tracking-tight md:text-2xl">
            🎬 <span className="text-red-500">
              CineMatch
            </span>
          </div>

          <div className="hidden text-sm text-gray-500 md:block">
            AI Movie Recommendation Engine
          </div>

        </div>

      </nav>


      {/* ====================================================
          CONTENT
      ==================================================== */}

      <div className="mx-auto max-w-[1450px] px-5 py-6 md:px-8">

        <Hero />


        {/* ==================================================
            SEARCH
        ================================================== */}

        <MovieSearch
          movies={movies}
          onRecommend={getRecommendations}
          loading={loading}
        />


        {/* ==================================================
            ERROR
        ================================================== */}

        {error && (

          <div className="mb-8 rounded-xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-300">
            {error}
          </div>

        )}


        {/* ==================================================
            RECOMMENDATIONS
        ================================================== */}

        {recommendations.length > 0 && (

          <section
            id="recommendations"
            className="pb-12"
          >

            <div className="mb-6">

              <h2 className="text-2xl font-extrabold md:text-3xl">

                Because you watched{" "}

                <span className="text-red-500">
                  {selectedMovie}
                </span>

              </h2>

              <div className="mt-3 h-1 w-12 rounded-full bg-red-600" />

            </div>

            <MovieGrid
              movies={recommendations}
            />

          </section>

        )}


        {/* ==================================================
            INITIAL STATE
        ================================================== */}

        {!loading &&
          recommendations.length === 0 &&
          !error && (

            <section className="border-t border-white/10 py-20 text-center">

              <div className="text-5xl">
                🍿
              </div>

              <h2 className="mt-5 text-2xl font-bold">
                Your recommendations are waiting
              </h2>

              <p className="mx-auto mt-3 max-w-md text-sm leading-6 text-gray-500">
                Choose a movie above and CineMatch
                will find movies with similar content.
              </p>

            </section>

          )}


        {/* ==================================================
            FOOTER
        ================================================== */}

        <footer className="border-t border-white/10 py-8 text-center text-xs text-gray-600">

          🎬 CineMatch
          {" • "}
          AI-Powered Movie Recommendation System

        </footer>

      </div>

    </main>

  );
}