import React, { useState, useEffect } from "react";
import axios from "axios";

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    axios.get("/leaderboard").then((response) => {
      setLeaderboard(response.data);
    });
  }, []);

  return (
    <div>
      <h1>Leaderboard</h1>
      <ul>
        {leaderboard.map((lb) => (
          <li key={lb.name}>
            {lb.name} - Rank: {lb.rank}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Leaderboard;
