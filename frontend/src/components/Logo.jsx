// Logo component with 655x480 resolution and multiple blue shades
export default function Logo({ width = 655, height = 480 }) {
  return (
    <svg
      width={width}
      height={height}
      viewBox="0 0 655 480"
      style={styles.svg}
      xmlns="http://www.w3.org/2000/svg"
    >
      {/* Background gradient with multiple blue shades */}
      <defs>
        <linearGradient id="blueGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style={{ stopColor: "#0066ff", stopOpacity: 1 }} />
          <stop offset="25%" style={{ stopColor: "#0099ff", stopOpacity: 1 }} />
          <stop offset="50%" style={{ stopColor: "#00aaff", stopOpacity: 1 }} />
          <stop offset="75%" style={{ stopColor: "#0099ff", stopOpacity: 1 }} />
          <stop offset="100%" style={{ stopColor: "#0055dd", stopOpacity: 1 }} />
        </linearGradient>
        
        <radialGradient id="blueShadow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" style={{ stopColor: "#00ccff", stopOpacity: 0.8 }} />
          <stop offset="100%" style={{ stopColor: "#0033aa", stopOpacity: 0.3 }} />
        </radialGradient>
      </defs>

      {/* Main envelope shape with multiple blue layers */}
      <g>
        {/* Outer envelope background */}
        <rect
          x="100"
          y="80"
          width="455"
          height="320"
          rx="20"
          style={{ fill: "url(#blueGradient)", filter: "drop-shadow(0 10px 30px rgba(0, 102, 255, 0.4))" }}
        />

        {/* Envelope flap - darkest blue */}
        <path
          d="M 100 80 L 327.5 220 L 555 80 Z"
          style={{ fill: "#0033aa", opacity: 0.9 }}
        />

        {/* Inner envelope flap - medium blue */}
        <path
          d="M 120 100 L 327.5 210 L 535 100 Z"
          style={{ fill: "#0055dd", opacity: 0.85 }}
        />

        {/* Letter/paper inside - light blue */}
        <rect
          x="130"
          y="140"
          width="395"
          height="240"
          rx="12"
          style={{ fill: "#00aaff", opacity: 0.6 }}
        />

        {/* Top paper line - light accent */}
        <rect
          x="150"
          y="160"
          width="355"
          height="8"
          rx="4"
          style={{ fill: "#00ccff", opacity: 0.7 }}
        />

        {/* Middle paper lines - medium accent */}
        <rect
          x="150"
          y="190"
          width="355"
          height="6"
          rx="3"
          style={{ fill: "#0099ff", opacity: 0.6 }}
        />
        <rect
          x="150"
          y="220"
          width="280"
          height="6"
          rx="3"
          style={{ fill: "#0099ff", opacity: 0.6 }}
        />
      </g>

      {/* Sparkle/glow effects */}
      <g>
        {/* Top right sparkle */}
        <circle cx="520" cy="110" r="8" style={{ fill: "#00ccff", opacity: 0.8 }} />
        <circle cx="520" cy="110" r="5" style={{ fill: "#ffffff", opacity: 0.6 }} />

        {/* Bottom left sparkle */}
        <circle cx="140" cy="360" r="6" style={{ fill: "#0099ff", opacity: 0.7 }} />
        <circle cx="140" cy="360" r="3" style={{ fill: "#ffffff", opacity: 0.5 }} />

        {/* Center accent sparkle */}
        <circle cx="327.5" cy="240" r="10" style={{ fill: "#00aaff", opacity: 0.6 }} />
        <circle cx="327.5" cy="240" r="6" style={{ fill: "#ffffff", opacity: 0.4 }} />
      </g>

      {/* Arrow/send indicator - medium blue */}
      <g>
        <path
          d="M 580 200 L 620 220 L 600 240 Z"
          style={{ fill: "#0099ff", filter: "drop-shadow(0 4px 12px rgba(0, 153, 255, 0.5))" }}
        />
      </g>
    </svg>
  )
}

const styles = {
  svg: {
    filter: "drop-shadow(0 8px 24px rgba(0, 102, 255, 0.3))",
    transition: "all 0.3s ease",
  },
}
