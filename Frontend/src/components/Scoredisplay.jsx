import React from 'react'
import Scorecircle from './Scorecircle';
function Scoredisplay({ score, hospital, distance }) {
  return (
    <div className="absolute bottom-6 left-6 z-[1000] w-72 p-5 rounded-2xl bg-white/70 backdrop-blur-lg shadow-xl border border-white/30">
      <h2 className="text-center text-gray-600 tracking-widest text-sm font-semibold">
        SCORE
      </h2>

      <Scorecircle score={score} />

      <div className="mt-4 text-sm text-gray-700 space-y-1">
        <p className="font-medium">Closest Health Center</p>
        <p className="text-gray-900">{hospital}</p>

        <p className="mt-2 font-medium">Distance</p>
        <p className="text-gray-900 font-semibold">
          {distance.toFixed(2)} KM
        </p>
      </div>
    </div>
  );
}
export default Scoredisplay;