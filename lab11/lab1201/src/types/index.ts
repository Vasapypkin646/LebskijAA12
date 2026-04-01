export interface GeoNote {
    id: string;
    title: string;
    content: string;
    latitude: number;
    longitude: number;
    address?: string;
    photoUri?: string;
    createdAt: number;
    updatedAt?: number;
}

export interface Location {
    latitude: number;
    longitude: number;
    address?: string;
}