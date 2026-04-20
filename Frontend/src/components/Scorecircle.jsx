function Scorecircle({ score }) {
  const radius = 60;
  const stroke = 10;
  const normalized = radius - stroke * 0.5;
  const circumference = normalized * 2 * Math.PI;

  const progress = score / 100;
  const strokeDashoffset = circumference - progress * circumference;

  const getColor = () => {
    if (score < 40) return "#ef4444";   
    if (score < 70) return "#f59e0b";   
    return "#22c55e";                   
  };

  return (
    <div className="flex justify-center items-center mt-3">
      <svg className="w-40 h-40">
        <circle
          className="text-gray-200"
          stroke="currentColor"
          fill="transparent"
          strokeWidth={stroke}
          r={normalized}
          cx="80"
          cy="80"
        />

        {/* progress circle */}
        <circle
          stroke={getColor()}
          fill="transparent"
          strokeWidth={stroke}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
          r={normalized}
          cx="80"
          cy="80"
          className="transition-all duration-500 ease-out"
        />

        {/* score text */}
        <text
          x="50%"
          y="50%"
          dominantBaseline="middle"
          textAnchor="middle"
          className="text-2xl font-bold fill-gray-800"
        >
          {score.toFixed(1)}
        </text>
      </svg>
    </div>
  );
}
export default Scorecircle;