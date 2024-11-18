import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useUploadClothes, useClothes, useInProgressClothes, useUpload } from '@/dashboard/clothes/clothes.query';
import {
  Card,
  Image,
  Text,
  Group,
  Button,
  Modal,
  FileInput,
  LoadingOverlay,
  Grid,
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';

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

  if (isLoading) return <LoadingOverlay visible={true} />;
  if (isError) return <Text>Failed to load clothes.</Text>;

  return (
    <div style={{ position: 'relative', padding: '20px' }}>
      <Group position="apart" style={{ marginBottom: '20px' }}>
        <Text size="xl" weight={700}>
          Your Clothes
        </Text>
        <Group>
          <FileInput
            placeholder="Upload your clothing"
            value={file}
            onChange={setFile}
            accept="image/*"
          />
          <Button onClick={handleUpload} disabled={!file}>
            Upload
          </Button>
        </Group>
      </Group>

      <Grid>
        {data?.clothes.map((cloth: ClothingItem) => (
          <Grid.Col span={4} key={cloth.id}>
            <Card shadow="sm" padding="lg" onClick={() => handleCardClick(cloth)} style={{ cursor: 'pointer' }}>
              <Card.Section>
                <Image src={`http://localhost:9000/uploads/${cloth.image}`} height={160} alt="Clothing Image" />
              </Card.Section>

              <Group position="apart" style={{ marginBottom: 5, marginTop: '10px' }}>
                <Text weight={500}>Status: {cloth.status}</Text>
              </Group>
            </Card>
          </Grid.Col>
        ))}
      </Grid>0

      <Modal opened={opened} onClose={close} title="Clothing Details">
        {selectedCloth && (
          <div>
            <Image src={`http://localhost:9000/uploads/${selectedCloth.image}`} height={200} alt="Clothing Image" />
            <Text><strong>Color:</strong> {selectedCloth.color || 'N/A'}</Text>
            <Text><strong>Garment Type:</strong> {selectedCloth.garment_type || 'N/A'}</Text>
            <Text><strong>Patterns:</strong> {selectedCloth.patterns || 'N/A'}</Text>
            <Text><strong>Look Type:</strong> {selectedCloth.look_type || 'N/A'}</Text>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Clothes;
