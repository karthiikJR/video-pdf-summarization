import React from 'react'

function Link() {
	return (
		
			<div className="max-w-md grow">
				<label htmlFor="website-url" className="block py-2 text-gray-400">
					Youtube Link
				</label>
				<div className="flex items-center text-gray-300 border border-gray-400 rounded-md">
					<div className="px-3 py-2.5 rounded-l-md bg-gray-600 border-r border-gray-400">
						https://
					</div>
					<input
						type="text"
						placeholder="www.youtube.com/watch?v=..."
						id="website-url"
						className="w-full p-2.5 ml-2 bg-transparent text-gray-300 outline-none"
						required
					/>
				</div>
			</div>
			

	);
}

export default Link