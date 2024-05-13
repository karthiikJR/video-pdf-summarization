import React, { useState } from 'react'

function PDFInput() {

	const [file, setFile] = useState(null);

	const onFileChange = (event) => {
		const selectedFile = event.target.files[0];
		setFile(selectedFile);
	};
	return (
		<>
			<div className="flex items-center text-gray-400 justify-center w-full">
				<label
					htmlFor="dropzone-file"
					className="flex flex-col items-center justify-center w-full h-64 border-2 border-gray-500 border-dashed rounded-lg cursor-pointer bg-gray-700 "
				>
					<div className="flex flex-col items-center justify-center pt-5 pb-6">
						<svg
							className="w-8 h-8 mb-4 text-gray-100"
							aria-hidden="true"
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 20 16"
						>
							<path
								stroke="currentColor"
								strokeLinecap="round"
								strokeLinejoin="round"
								strokeWidth="2"
								d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
							/>
						</svg>
						<p className="mb-2 text-sm ">
							<span className="font-semibold">Click to upload</span> or drag and drop
						</p>
						<p className="text-xs ">
							PDF file only, max size 10MB
						</p>
					</div>
					<input onChange={onFileChange} id="dropzone-file" type="file" className="hidden" accept="application/pdf" />
				</label>
			</div>
			{(file) &&
				<div className="flex flex-col items-center justify-center w-full">
					<h1 className='text-xl text-gray-300 font-bold'>PDF Loaded</h1>
					<p className="text-xs text-gray-400">{file.name}</p>
				</div>

			}
		</>
	);
}

export default PDFInput