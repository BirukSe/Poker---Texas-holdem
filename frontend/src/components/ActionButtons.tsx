'use client'
import { Button } from "@/components/ui/button"
import { useState } from "react"

export default function ActionButtons({
  onAction,
}: {
  onAction: (action: string, value?: number) => void
}) {
  const [bet, setBet] = useState(20)
  const [raise, setRaise] = useState(40)

  return (
    <div className="flex gap-2 flex-wrap mt-6">
      <Button className="bg-blue-500" onClick={() => onAction("f")}>Fold</Button>
      <Button className="bg-green-500" onClick={() => onAction("x")}>Check</Button>
      <Button className="bg-green-500" onClick={() => onAction("c")}>Call</Button>

      {/* Bet */}
      <div className="flex items-center gap-1">
        <Button className="bg-yellow-500" onClick={() => onAction("b", bet)}>Bet {bet}</Button>
        <Button className="bg-yellow-500" size="sm" onClick={() => setBet((v) => v + 10)}>+</Button>
        <Button className="bg-yellow-500" size="sm" onClick={() => setBet((v) => Math.max(0, v - 10))}>-</Button>
      </div>

      {/* Raise */}
      <div className="flex items-center gap-1">
        <Button className="bg-yellow-500" onClick={() => onAction("r", raise)}>Raise {raise}</Button>
        <Button className="bg-yellow-500" size="sm" onClick={() => setRaise((v) => v + 10)}>+</Button>
        <Button className="bg-yellow-500" size="sm" onClick={() => setRaise((v) => Math.max(0, v - 10))}>-</Button>
      </div>

      <Button className="bg-red-600" onClick={() => onAction("allin")}>ALLIN</Button>
    </div>
  )
}
