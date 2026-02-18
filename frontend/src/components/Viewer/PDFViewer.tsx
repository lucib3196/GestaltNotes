type PDFViewerProps = {
    src: string;
};

export function PDFViewer({ src }: PDFViewerProps) {
    return (
        <div className="w-full h-125 border rounded-lg overflow-hidden">
            <iframe
                src={src}
                className="w-full h-full"
                title="Lecture PDF"
            />
        </div>
    );
}