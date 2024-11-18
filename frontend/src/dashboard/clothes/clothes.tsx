import React, { useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { useUploadClothes, useClothes } from '@/dashboard/clothes/clothes.query';
import { Modal, FileInput, LoadingOverlay, Button } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import styles from './clothes.module.scss';

interface ClothingItem {
  id: string;
  image: string;
  status: string;
  color?: string | null;
  garment_type?: string | null;
  patterns?: string | null;
  look_type?: string | null;
}

const Clothes: React.FC = () => {
  const queryClient = useQueryClient();
  const { data, isLoading, isError } = useClothes({});
  const [opened, { open, close }] = useDisclosure(false);
  const [selectedCloth, setSelectedCloth] = useState<ClothingItem | null>(null);
  const [file, setFile] = useState<File | null>(null);

  const handleUpload = async () => {
    if (file) {
        const fileBytes = await file.arrayBuffer();
        const fileBuffer = Buffer.from(fileBytes).toString('base64');
        await useUploadClothes.apiCall({ imageName: file.name, imageBuffer: fileBuffer });
        queryClient.invalidateQueries({ queryKey: ['clothes'] });
        setFile(null);
    }
    else {
        console.error("No file selected");
    }
  };

  const handleCardClick = async (cloth: ClothingItem) => {
    setSelectedCloth(cloth);
    open();
  };

  const getStatusClass = (status: string) => {
    return status.toLowerCase() === 'processing' 
      ? styles['status-processing']
      : styles['status-completed'];
  };

  if (isLoading) return <LoadingOverlay visible={true} />;
  if (isError) return <div className="text-red-600">Failed to load clothes.</div>;

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1 className={styles.title}>Your Clothes</h1>
        <div className={styles['upload-group']}>
          <FileInput
            placeholder="Upload your clothing"
            value={file}
            onChange={setFile}
            accept="image/*"
          />
          <Button onClick={handleUpload} disabled={!file}>
            Upload
          </Button>
        </div>
      </div>

      <div className={styles.grid}>
        {data?.clothes.map((cloth: ClothingItem) => (
          <div key={cloth.id} className={styles.card} onClick={() => handleCardClick(cloth)}>
            <div className={styles['card-image-wrapper']}>
              <img 
                src={`http://localhost:9000/uploads/${cloth.image}`}
                alt="Clothing Item"
                className={styles['card-image']}
              />
            </div>
            <div className={styles['card-content']}>
              <span className={`${styles['status-badge']} ${getStatusClass(cloth.status)}`}>
                {cloth.status}
              </span>
            </div>
          </div>
        ))}
      </div>

      <Modal opened={opened} onClose={close} title="Clothing Details" size="lg">
        {selectedCloth && (
          <div className={styles['modal-content']}>
            <div className={styles['modal-image']}>
              <img
                src={`http://localhost:9000/uploads/${selectedCloth.image}`}
                alt="Clothing Detail"
              />
            </div>
            {['color', 'garmentType', 'patterns', 'lookType'].map((field) => (
              <div key={field} className={styles['detail-row']}>
                <span className={styles['detail-label']}>
                  {field.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}:
                </span>
                <span className={styles['detail-value']}>
                  {selectedCloth[field as keyof ClothingItem] || 'N/A'}
                </span>
              </div>
            ))}
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Clothes;
