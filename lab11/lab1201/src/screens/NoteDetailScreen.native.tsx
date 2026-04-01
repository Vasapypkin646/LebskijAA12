import React from 'react';
import {
    View,
    Text,
    StyleSheet,
    ScrollView,
    TouchableOpacity,
    Alert
} from 'react-native';
import { useAppDispatch, useAppSelector } from '../hooks/reduxHooks';
import { removeNote } from '../store/notesSlice';

interface NoteDetailScreenProps {
    navigation: any;
    route: any;
}

const NoteDetailScreen: React.FC<NoteDetailScreenProps> = ({ navigation, route }) => {
    const { noteId } = route.params;
    const dispatch = useAppDispatch();
    const note = useAppSelector(state =>
        state.notes.items.find(item => item.id === noteId)
    );

    if (!note) {
        navigation.goBack();
        return null;
    }

    const handleDelete = () => {
        Alert.alert(
            'Удаление заметки',
            'Вы уверены, что хотите удалить эту заметку?',
            [
                { text: 'Отмена', style: 'cancel' },
                {
                    text: 'Удалить',
                    style: 'destructive',
                    onPress: async () => {
                        try {
                            await dispatch(removeNote(noteId)).unwrap();
                            navigation.goBack();
                        } catch (error) {
                            Alert.alert('Ошибка', 'Не удалось удалить заметку');
                        }
                    }
                }
            ]
        );
    };

    return (
        <ScrollView style={styles.container}>
            <View style={styles.header}>
                <Text style={styles.title}>{note.title}</Text>
                <Text style={styles.date}>
                    {new Date(note.createdAt).toLocaleString()}
                </Text>
            </View>

            <View style={styles.contentContainer}>
                <Text style={styles.content}>{note.content}</Text>
            </View>

            {note.address && (
                <View style={styles.addressContainer}>
                    <Text style={styles.addressLabel}>📍 Адрес:</Text>
                    <Text style={styles.addressText}>{note.address}</Text>
                </View>
            )}

            <View style={styles.coordinatesContainer}>
                <Text style={styles.coordinatesLabel}>📍 Координаты:</Text>
                <Text style={styles.coordinatesText}>
                    {note.latitude.toFixed(6)}, {note.longitude.toFixed(6)}
                </Text>
            </View>

            {note.photoUri && (
                <View style={styles.photoContainer}>
                    <Text style={styles.photoLabel}>📷 Фото сохранено</Text>
                </View>
            )}

            <TouchableOpacity style={styles.deleteButton} onPress={handleDelete}>
                <Text style={styles.deleteButtonText}>Удалить заметку</Text>
            </TouchableOpacity>
        </ScrollView>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5f5f5'
    },
    header: {
        backgroundColor: 'white',
        padding: 20,
        borderBottomWidth: 1,
        borderBottomColor: '#eee'
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        color: '#333',
        marginBottom: 8
    },
    date: {
        fontSize: 14,
        color: '#666'
    },
    contentContainer: {
        backgroundColor: 'white',
        padding: 20,
        marginTop: 1
    },
    content: {
        fontSize: 16,
        color: '#333',
        lineHeight: 24
    },
    addressContainer: {
        backgroundColor: 'white',
        padding: 20,
        marginTop: 1
    },
    addressLabel: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#333',
        marginBottom: 4
    },
    addressText: {
        fontSize: 14,
        color: '#007AFF'
    },
    coordinatesContainer: {
        backgroundColor: 'white',
        padding: 20,
        marginTop: 1
    },
    coordinatesLabel: {
        fontSize: 14,
        fontWeight: 'bold',
        color: '#333',
        marginBottom: 4
    },
    coordinatesText: {
        fontSize: 14,
        color: '#666'
    },
    photoContainer: {
        backgroundColor: 'white',
        padding: 20,
        marginTop: 1
    },
    photoLabel: {
        fontSize: 14,
        color: '#666',
        textAlign: 'center'
    },
    deleteButton: {
        backgroundColor: '#ff3b30',
        margin: 20,
        padding: 16,
        borderRadius: 8,
        alignItems: 'center'
    },
    deleteButtonText: {
        color: 'white',
        fontWeight: 'bold',
        fontSize: 16
    }
});

export default NoteDetailScreen;
