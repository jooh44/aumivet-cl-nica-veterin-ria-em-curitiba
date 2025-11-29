export default function NotFound() {
  return (
    <div className="min-h-screen bg-aumivet-white flex items-center justify-center px-4">
      <div className="text-center">
        <h1 className="text-9xl font-sans font-bold text-aumivet-pink mb-4">
          404
        </h1>
        <h2 className="text-3xl font-sans font-bold text-aumivet-black mb-4">
          Página Não Encontrada
        </h2>
        <p className="text-xl text-aumivet-gray mb-8">
          Desculpe, a página que você procura não existe.
        </p>
        <a
          href="/"
          className="inline-block bg-aumivet-green hover:bg-aumivet-green-light text-white px-8 py-3 rounded-lg font-sans font-semibold transition"
        >
          Voltar para Home
        </a>
      </div>
    </div>
  );
}
