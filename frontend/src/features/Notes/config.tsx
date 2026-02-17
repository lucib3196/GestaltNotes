import {type  Components } from "react-markdown";

export const markdownComponents: Components = {
    h1: ({ children }) => (
        <h1 className="text-4xl font-bold tracking-tight mb-6">
            {children}
        </h1>
    ),

    h2: ({ children }) => (
        <h2 className="text-2xl font-semibold mt-8 mb-4">
            {children}
        </h2>
    ),

    h3: ({ children }) => (
        <h3 className="text-xl font-medium mt-6 mb-3">
            {children}
        </h3>
    ),

    p: ({ children }) => (
        <p className="text-gray-700 leading-relaxed mb-4">
            {children}
        </p>
    ),

    ul: ({ children }) => (
        <ul className="list-disc pl-6 space-y-2 mb-4">
            {children}
        </ul>
    ),

    li: ({ children }) => (
        <li className="text-gray-700">
            {children}
        </li>
    ),
    blockquote: ({ children }) => (
        <blockquote className="border-l-4 border-gray-300 pl-4 italic text-gray-600 my-4">
            {children}
        </blockquote>
    ),

    strong: ({ children }) => (
        <strong className="font-semibold text-gray-900">
            {children}
        </strong>
    ),

    em: ({ children }) => (
        <em className="italic text-gray-800">
            {children}
        </em>
    ),
}