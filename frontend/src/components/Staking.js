import React, { useState } from "react";
import axios from "axios";

function Staking() {
  const [amount, setAmount] = useState(0);

  const handleStake = () => {
    axios.post("/stake", { amount }).then((response) => {
      alert(response.data.message);
    });
  };

  return (
    <div>
      <h1>Staking Interface</h1>
      <input
        type="number"
        value={amount}
        onChange={(e) => setAmount(e.target.value)}
        placeholder="Amount to Stake"
      />
      <button onClick={handleStake}>Stake</button>
    </div>
  );
}

export default Staking;
