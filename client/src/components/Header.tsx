export default function Header() {
  return (
    <header className="relative pt-16 text-center">
      <div className="inline-block mb-6">
        <div className="relative group">
          <div className="absolute -inset-1 bg-gradient-to-r from-blue-600 to-cyan-600 rounded-2xl blur-lg opacity-50 group-hover:opacity-100 transition duration-500" />
          <div className="relative w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center shadow-2xl">
            <span className="text-white font-black text-2xl">H</span>
          </div>
        </div>
      </div>

      <h1 className="text-6xl md:text-7xl font-black mb-4 text-white text-balance tracking-tight">
        <span className="bg-gradient-to-r from-blue-300 via-cyan-300 to-blue-300 bg-clip-text text-transparent">
          HelpSort
        </span>
      </h1>

      <p className="text-2xl md:text-3xl font-bold text-gray-300 mb-3">
        AI Support Intelligence
      </p>

      <p className="text-base md:text-lg text-gray-500 max-w-3xl mx-auto leading-relaxed">
        Intelligent ticket classification and routing using advanced NLP
        technology.
      </p>
    </header>
  );
}
