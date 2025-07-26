import React from 'react'

interface TestimonialCardProps {
  name: string;
  feedback: string;
}

function TestimonialCard({ name, feedback }: TestimonialCardProps) {
  return (
    <div className="bg-neutral-900 border border-gray-700 rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 p-6 h-[16rem] w-full flex flex-col justify-between">
      <div className="flex-1">
        <div className="text-blue-400 text-2xl mb-3">&quot;</div>
        <p className="text-gray-300 text-sm leading-relaxed line-clamp-4">
          {feedback}
        </p>
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-700">
        <div className="flex items-center">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-sm font-semibold">
            {name.charAt(0)}
          </div>
          <div className="ml-3">
            <p className="text-white font-medium text-sm">{name}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TestimonialCard