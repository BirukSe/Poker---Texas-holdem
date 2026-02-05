'use client'

import { useState } from "react"
import StackControl from "@/components/StackControl"
import ActionLog from "@/components/ActionLog"
import ActionButtons from "@/components/ActionButtons"
import HandHistory from "@/components/HandHistory"

export default function Home() {
  const [stack, setStack] = useState(10000)
  const [log, setLog] = useState<string[]>([])
  const [hands, setHands] = useState<string[]>([])
  const [currentPlayerIndex, setCurrentPlayerIndex] = useState(0) // Optional: update this with actual logic

  const makeApiRequest = async (
    endpoint: string,
    method: 'GET' | 'POST' = 'POST',
    body?: Record<string, any>
  ): Promise<any> => {
    const response = await fetch(`http://127.0.0.1:8000${endpoint}`, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`)
    }

    return response.json()
  }

  const handleApply = async (value: number) => {
    setStack(value)

    try {
      const data = await makeApiRequest('/hand/start/game', 'POST', { stack_size: value })

      const { dealer_index, small_blind_index, big_blind_index, preflop_dealings } = data.cards

      const formattedLog: string[] = []

      preflop_dealings.forEach((card: string, index: number) => {
        formattedLog.push(`Player ${index + 1} is dealt ${card}`)
      })

      formattedLog.push('---')
      formattedLog.push(`Player ${dealer_index + 1} is the dealer`)
      formattedLog.push(`Player ${small_blind_index + 1} posts small blind - 20 chips`)
      formattedLog.push(`Player ${big_blind_index + 1} posts big blind - 40 chips`)
      formattedLog.push('---')

      setLog(prev => [...prev, ...formattedLog])
    } catch (error) {
      setLog(prev => [...prev, `Error: ${error}`])
    }
  }

  const handleReset = () => {
    setStack(10000)
    setLog(prev => [...prev, `Stack reset to 10000`])
  }

  const handleAction = async (action: string, value?: number) => {
    const actionStr = value !== undefined ? `${action}${value}` : action
    let endpoint = ''
    let displayAction = ''

    if (action === 'f') {
      endpoint = '/hand/action/fold'
      displayAction = 'folds'
    } else if (action === 'x' || action === 'c') {
      endpoint = '/hand/action/check_or_call'
      displayAction = action === 'x' ? 'checks' : 'calls'
    } else if (action === 'b' || action === 'r') {
      endpoint = '/hand/action/complete_bet_or_raise_to'
      displayAction = action === 'b'
        ? `bets ${value} chips`
        : `raises to ${value} chips`
    } else if (action === 'allin') {
      endpoint = '/hand/action/complete_bet_or_raise_to'
      displayAction = 'goes all-in'
    }

    try {
      await makeApiRequest(endpoint, 'POST', {
        action: actionStr,
        amount: value,
      })

      setLog(prev => [...prev, `Player ${currentPlayerIndex + 1} ${displayAction}`])
      // Update current player index here if necessary
    } catch (error) {
      setLog(prev => [...prev, `Error: ${error}`])
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-slate-800">Texas Hold'em Trainer</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Panel - Hand History (swapped) */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-slate-700">Game History</h2>
            <div className="bg-slate-50 p-4 rounded border border-slate-200 h-[600px] overflow-y-auto">
              <HandHistory
                hands={hands.length ? hands : [
                  `Hand #395b5999-cdc1-4469-947e-649d30aa6158
Stack 10000; Dealer: Player 3; Player 4 Small Blind; Player 6
Hands: Player 1: Tc2c; Player 2: 5d4c; Player 3: AhAs; Player 4: QcTd
Actions: ffrr300cT 3hKdQs xx0100c Ac xx Th bb80r160c
Winnings: Player 1: -40; Player 2: 0; Player 3: -560; Player 4: +600`
                ]}
              />
            </div>
          </div>

          {/* Right Panel - Controls (swapped) */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4 text-slate-700">Game Controls</h2>
            <StackControl defaultStack={stack} onApply={handleApply} onReset={handleReset} />

            <h3 className="text-lg font-semibold mt-6 mb-2 text-slate-600">Activity Log</h3>
            <ActionLog log={log} />

            <h3 className="text-lg font-semibold mt-6 mb-2 text-slate-600">Player Actions</h3>
            <ActionButtons onAction={handleAction} />
          </div>
        </div>
      </div>
    </div>
  )
}
