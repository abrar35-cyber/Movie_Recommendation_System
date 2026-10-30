export default function Hero() {
  return (
    <section
      className="relative mb-12 min-h-[500px] overflow-hidden rounded-2xl border border-white/10"
      style={{
        backgroundImage:
          "linear-gradient(90deg, rgba(5,7,10,0.98) 0%, rgba(5,7,10,0.85) 35%, rgba(5,7,10,0.35) 70%, rgba(5,7,10,0.8) 100%), linear-gradient(0deg, rgba(5,7,10,0.95), transparent 60%), url('https://image.tmdb.org/t/p/original/8bcoRX3hQRHufLPSDREdvr3YjWC.jpg')",
        backgroundSize: "cover",
        backgroundPosition: "center"
      }}
    >

      <div className="flex min-h-[500px] items-end p-8 md:p-14">

        <div className="max-w-2xl">

          <span className="mb-5 inline-block rounded bg-red-600 px-3 py-2 text-xs font-black tracking-widest">
            AI MOVIE DISCOVERY
          </span>

          <h1 className="text-4xl font-black leading-none tracking-tight md:text-7xl">
            Discover your next obsession.
          </h1>

          <p className="mt-6 max-w-xl text-base leading-7 text-gray-300 md:text-lg">
            Find movies that match your taste using content-based
            machine learning and intelligent similarity matching.
          </p>

          <div className="mt-6 flex flex-wrap gap-5 text-sm font-semibold text-gray-300">

            <span>🎬 4,800+ Movies</span>

            <span className="text-yellow-400">
              ★ AI Powered
            </span>

            <span>⚡ Instant Recommendations</span>

          </div>

        </div>

      </div>

    </section>
  );
}