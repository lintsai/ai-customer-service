"use client";

import dynamic from 'next/dynamic'

// 動態導入 Chat 組件並禁用 SSR
const Chat = dynamic(() => import('@/components/Chat'), {
  ssr: false,
  loading: () => (
    <div className="flex items-center justify-center min-h-screen">
      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
    </div>
  ),
})

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-100">
      <Chat />
    </main>
  )
}