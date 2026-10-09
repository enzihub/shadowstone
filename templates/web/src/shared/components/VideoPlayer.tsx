export const VideoPlayer = () => {
  return (
    <div className='relative mx-auto mb-8 aspect-video w-full max-w-2xl overflow-hidden rounded-lg px-12'>
      <iframe
        className='absolute left-0 top-0 h-full w-full'
        src='https://komododecks.com/embed/recordings/TAd7DPdlnSU5RZQUqein'
        title='YouTube video player'
        allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture'
        allowFullScreen
      />
    </div>
  );
};
