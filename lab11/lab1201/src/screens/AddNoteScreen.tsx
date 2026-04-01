import * as ImagePicker from 'expo-image-picker';
import * as Location from 'expo-location';
import React, { useEffect, useState } from 'react';
import {
    ActivityIndicator,
    Alert,
    ScrollView,
    StyleSheet,
    Text,
    TextInput,
    TouchableOpacity,
    View
} from 'react-native';
import 'react-native-get-random-values';
import { v4 as uuidv4 } from 'uuid';
import { useAppDispatch } from '../hooks/reduxHooks';
import { saveNote } from '../store/notesSlice';
import { GeoNote } from '../types';

interface AddNoteScreenProps {
    navigation: any;
}

const AddNoteScreen: React.FC<AddNoteScreenProps> = ({ navigation }) => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');
    const [address, setAddress] = useState<string | undefined>();
    const [photoUri, setPhotoUri] = useState<string | undefined>();
    const [isLoading, setIsLoading] = useState(false);
    const [isSaving, setIsSaving] = useState(false);
    const [location, setLocation] = useState<{ latitude: number; longitude: number } | null>(null);
    
    const dispatch = useAppDispatch();

    useEffect(() => {
        getCurrentLocation();
        requestPermissions();
    }, []);

    const requestPermissions = async () => {
        const cameraPermission = await ImagePicker.requestCameraPermissionsAsync();
        if (!cameraPermission.granted) {
            Alert.alert('Внимание', 'Необходимо разрешение на использование камеры');
        }
    };

    const getCurrentLocation = async () => {
        setIsLoading(true);
        try {
            const { status } = await Location.requestForegroundPermissionsAsync();
            if (status !== 'granted') {
                Alert.alert('Ошибка', 'Нет доступа к геолокации');
                return;
            }

            const currentLocation = await Location.getCurrentPositionAsync({});
            setLocation({
                latitude: currentLocation.coords.latitude,
                longitude: currentLocation.coords.longitude
            });

            const addresses = await Location.reverseGeocodeAsync({
                latitude: currentLocation.coords.latitude,
                longitude: currentLocation.coords.longitude
            });

            if (addresses.length > 0) {
                const addr = addresses[0];
                const addressString = [
                    addr.street,
                    addr.district,
                    addr.city,
                    addr.country
                ].filter(Boolean).join(', ');
                setAddress(addressString);
            }
        } catch (error) {
            console.error('Error getting location:', error);
            Alert.alert('Ошибка', 'Не удалось получить местоположение');
        } finally {
            setIsLoading(false);
        }
    };

    const takePhoto = async () => {
        try {
            const result = await ImagePicker.launchCameraAsync({
                mediaTypes: ImagePicker.MediaTypeOptions.Images,
                allowsEditing: true,
                quality: 0.8
            });

            if (!result.canceled && result.assets && result.assets.length > 0) {
                setPhotoUri(result.assets[0].uri);
            }
        } catch (error) {
            console.error('Error taking photo:', error);
            Alert.alert('Ошибка', 'Не удалось сделать фото');
        }
    };

    const handleSave = async () => {
        if (!title.trim()) {
            Alert.alert('Ошибка', 'Введите заголовок заметки');
            return;
        }

        if (!content.trim()) {
            Alert.alert('Ошибка', 'Введите содержание заметки');
            return;
        }

        if (!location) {
            Alert.alert('Ошибка', 'Не удалось определить местоположение');
            return;
        }

        setIsSaving(true);

        const newNote: GeoNote = {
            id: uuidv4(),
            title: title.trim(),
            content: content.trim(),
            latitude: location.latitude,
            longitude: location.longitude,
            address,
            photoUri,
            createdAt: Date.now()
        };

        try {
            // TODO: Диспатчить действие saveNote
            await dispatch(saveNote(newNote)).unwrap();
            
            Alert.alert('Успех', 'Заметка сохранена', [
                { text: 'OK', onPress: () => navigation.goBack() }
            ]);
        } catch (error) {
            Alert.alert('Ошибка', 'Не удалось сохранить заметку');
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.form}>
                <Text style={styles.label}>Заголовок</Text>
                <TextInput
                    style={styles.input}
                    value={title}
                    onChangeText={setTitle}
                    placeholder="Введите заголовок"
                />

                <Text style={styles.label}>Содержание</Text>
                <TextInput
                    style={[styles.input, styles.textArea]}
                    value={content}
                    onChangeText={setContent}
                    placeholder="Введите содержание"
                    multiline
                    numberOfLines={5}
                    textAlignVertical="top"
                />

                <View style={styles.locationContainer}>
                    <Text style={styles.label}>Местоположение</Text>
                    {isLoading ? (
                        <ActivityIndicator size="small" color="#007AFF" />
                    ) : location ? (
                        <View>
                            <Text style={styles.locationText}>
                                📍 {address || `${location.latitude.toFixed(4)}, ${location.longitude.toFixed(4)}`}
                            </Text>
                            <TouchableOpacity
                                style={styles.refreshButton}
                                onPress={getCurrentLocation}
                            >
                                <Text style={styles.refreshButtonText}>Обновить</Text>
                            </TouchableOpacity>
                        </View>
                    ) : (
                        <TouchableOpacity
                            style={styles.locationButton}
                            onPress={getCurrentLocation}
                        >
                            <Text style={styles.locationButtonText}>Получить местоположение</Text>
                        </TouchableOpacity>
                    )}
                </View>

                <View style={styles.photoContainer}>
                    <Text style={styles.label}>Фото</Text>
                    <TouchableOpacity
                        style={styles.photoButton}
                        onPress={takePhoto}
                    >
                        <Text style={styles.photoButtonText}>
                            {photoUri ? '📸 Фото добавлено' : '📷 Сделать фото'}
                        </Text>
                    </TouchableOpacity>
                </View>

                <TouchableOpacity
                    style={[
                        styles.saveButton,
                        (!title.trim() || !content.trim() || !location || isSaving) && styles.saveButtonDisabled
                    ]}
                    onPress={handleSave}
                    disabled={!title.trim() || !content.trim() || !location || isSaving}
                >
                    {isSaving ? (
                        <ActivityIndicator color="white" />
                    ) : (
                        <Text style={styles.saveButtonText}>Сохранить</Text>
                    )}
                </TouchableOpacity>
            </View>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5f5f5'
    },
    form: {
        padding: 16
    },
    label: {
        fontSize: 16,
        fontWeight: 'bold',
        marginBottom: 8,
        color: '#333'
    },
    input: {
        backgroundColor: 'white',
        borderRadius: 8,
        padding: 12,
        marginBottom: 16,
        borderWidth: 1,
        borderColor: '#ddd'
    },
    textArea: {
        minHeight: 100
    },
    locationContainer: {
        marginBottom: 16
    },
    locationText: {
        fontSize: 14,
        color: '#007AFF',
        marginBottom: 8
    },
    refreshButton: {
        alignSelf: 'flex-start',
        paddingHorizontal: 12,
        paddingVertical: 6,
        backgroundColor: '#e1f5fe',
        borderRadius: 4
    },
    refreshButtonText: {
        color: '#007AFF',
        fontSize: 12
    },
    locationButton: {
        backgroundColor: '#e1f5fe',
        padding: 12,
        borderRadius: 8,
        alignItems: 'center'
    },
    locationButtonText: {
        color: '#007AFF',
        fontWeight: 'bold'
    },
    photoContainer: {
        marginBottom: 24
    },
    photoButton: {
        backgroundColor: '#e1f5fe',
        padding: 12,
        borderRadius: 8,
        alignItems: 'center'
    },
    photoButtonText: {
        color: '#007AFF',
        fontWeight: 'bold'
    },
    saveButton: {
        backgroundColor: '#007AFF',
        padding: 16,
        borderRadius: 8,
        alignItems: 'center',
        marginTop: 16
    },
    saveButtonDisabled: {
        backgroundColor: '#ccc'
    },
    saveButtonText: {
        color: 'white',
        fontWeight: 'bold',
        fontSize: 16
    }
});

export default AddNoteScreen;