import {useNavigate} from "react-router-dom";

const Hero = () => {
    const navigate = useNavigate();

    return (
        <div className="relative flex items-center justify-center min-h-screen px-4 text-center ">
            <div className="relative z-10 flex flex-col items-center w-full overflow-visible">
                {/* Wavify Heading */}
                <h1 className="text-[120px] xs:text-7xl md:text-9xl lg:text-[120px] xl:text-[160px] 2xl:text-[200px]
                font-bold font-pacifico text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 via-red-500 to-purple-500 p-18 md:p-20">
                    Wavify
                </h1>

                {/* Tagline */}
                <h2 className="text-2xl xs:text-3xl sm:text-4xl md:text-5xl font-bold leading-snug text-transparent
                bg-clip-text bg-gradient-to-r from-pink-400 to-blue-500 ">
                    Your Music, Your Vibe
                </h2>

                <button
                    onClick={() => navigate('/play')}
                    className="mt-6 px-6 py-3 bg-gradient-to-r from-blue-500 to-indigo-600
    text-white text-lg font-semibold rounded-3xl shadow-md transition-all duration-500 ease-in-out
    hover:bg-gradient-to-r hover:from-indigo-600 hover:to-purple-500 transform hover:scale-105"
                >
                    Start Listening
                </button>

            </div>
        </div>
    );
};

export default Hero;
