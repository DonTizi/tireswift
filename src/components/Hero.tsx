'use client'
import React, { useState } from 'react';
import Modal from 'react-modal';
import { Button } from '@/components/Button';
import { Container } from '@/components/Container';

Modal.setAppElement('#root'); // Remplacez '#root' par l'ID de votre élément racine

export function Hero() {
  const [modalIsOpen, setModalIsOpen] = useState(false);

  function openModal() {
    setModalIsOpen(true);
  }

  function closeModal() {
    setModalIsOpen(false);
  }

  return (
    <Container className="pb-16 pt-20 text-center lg:pt-32">
      <h1 className="mx-auto max-w-4xl font-display text-5xl font-medium tracking-tight text-slate-900 sm:text-7xl">
        Tire Changing{' '}
        <span className="relative whitespace-nowrap text-blue-600">
          <span className="relative">made simple</span>
        </span>
        {' '}for you.
      </h1>
      <p className="mx-auto mt-6 max-w-2xl text-lg tracking-tight text-slate-700">
        Optimize your schedule and your income in real time.
      </p>
      <div className="mt-10 flex justify-center gap-x-6">
        <Button href="/register">Try it for free.</Button>
        <Button onClick={openModal} variant="outline">
          Watch video
        </Button>
      </div>

      <Modal isOpen={modalIsOpen} onRequestClose={closeModal} contentLabel="Video Modal" style={{ content: { top: '50%', left: '50%', right: 'auto', bottom: 'auto', marginRight: '-50%', transform: 'translate(-50%, -50%)' } }}>
        <h2>Video Title</h2>
        <button onClick={closeModal}>close</button>
        <div>
          <video width="100%" height="auto" controls>
            <source src="path_to_your_video.mp4" type="video/mp4" />
            Votre navigateur ne supporte pas la balise vidéo.
          </video>
        </div>
      </Modal>
    </Container>
  );
}
