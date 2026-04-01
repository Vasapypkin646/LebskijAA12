import React, { useEffect } from 'react';
import {
    ActivityIndicator,
    FlatList,
    StyleSheet,
    Text,
    TouchableOpacity,
    View
} from 'react-native';
import { useAppDispatch, useAppSelector } from '../hooks/reduxHooks';
import { loadNotes } from '../store/notesSlice';

interface NotesListScreenProps {
    navigation: any;
}

const NotesListScreen: React.FC<NotesListScreenProps> = ({ navigation }) => {
    const dispatch = useAppDispatch();
    const { items: notes, loading, error } = useAppSelector(state => state.notes);

    useEffect(() => {
        dispatch(loadNotes());
    }, [dispatch]);

    const renderNoteItem = ({ item }: any) => (
        <TouchableOpacity
            style={styles.noteItem}
            onPress={() => navigation.navigate('NoteDetail', { noteId: item.id })}
        >
            <View style={styles.noteHeader}>
                <Text style={styles.noteTitle}>{item.title}</Text>
                <Text style={styles.noteDate}>
                    {new Date(item.createdAt).toLocaleDateString()}
                </Text>
            </View>
            <Text style={styles.noteContent} numberOfLines={2}>
                {item.content}
            </Text>
            {item.address && (
                <Text style={styles.noteAddress} numberOfLines={1}>
                    📍 {item.address}
                </Text>
            )}
            {item.photoUri && (
                <View style={styles.photoBadge}>
                    <Text style={styles.photoBadgeText}>📷</Text>
                </View>
            )}
        </TouchableOpacity>
    );

    if (loading) {
        return (
            <View style={styles.centerContainer}>
                <ActivityIndicator size="large" color="#007AFF" />
            </View>
        );
    }

    if (error) {
        return (
            <View style={styles.centerContainer}>
                <Text style={styles.errorText}>Ошибка: {error}</Text>
                <TouchableOpacity
                    style={styles.retryButton}
                    onPress={() => dispatch(loadNotes())}
                >
                    <Text style={styles.retryText}>Повторить</Text>
                </TouchableOpacity>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            {notes.length === 0 ? (
                <View style={styles.emptyContainer}>
                    <Text style={styles.emptyText}>Нет заметок</Text>
                    <Text style={styles.emptySubtext}>
                        Нажмите + чтобы создать первую заметку
                    </Text>
                </View>
            ) : (
                <FlatList
                    data={notes}
                    renderItem={renderNoteItem}
                    keyExtractor={item => item.id}
                    contentContainerStyle={styles.listContent}
                />
            )}
            
            <TouchableOpacity
                style={styles.fab}
                onPress={() => navigation.navigate('AddNote')}
            >
                <Text style={styles.fabText}>+</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f5f5f5'
    },
    centerContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#f5f5f5'
    },
    listContent: {
        padding: 16
    },
    noteItem: {
        backgroundColor: 'white',
        borderRadius: 8,
        padding: 16,
        marginBottom: 12,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3
    },
    noteHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 8
    },
    noteTitle: {
        fontSize: 16,
        fontWeight: 'bold',
        flex: 1
    },
    noteDate: {
        fontSize: 12,
        color: '#666',
        marginLeft: 8
    },
    noteContent: {
        fontSize: 14,
        color: '#333',
        marginBottom: 8
    },
    noteAddress: {
        fontSize: 12,
        color: '#007AFF'
    },
    photoBadge: {
        position: 'absolute',
        top: 16,
        right: 16,
        backgroundColor: '#007AFF',
        borderRadius: 12,
        paddingHorizontal: 8,
        paddingVertical: 4
    },
    photoBadgeText: {
        color: 'white',
        fontSize: 12
    },
    emptyContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        paddingHorizontal: 32
    },
    emptyText: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#333',
        marginBottom: 8
    },
    emptySubtext: {
        fontSize: 14,
        color: '#666',
        textAlign: 'center'
    },
    errorText: {
        fontSize: 16,
        color: 'red',
        marginBottom: 16
    },
    retryButton: {
        paddingHorizontal: 20,
        paddingVertical: 10,
        backgroundColor: '#007AFF',
        borderRadius: 8
    },
    retryText: {
        color: 'white',
        fontWeight: 'bold'
    },
    fab: {
        position: 'absolute',
        bottom: 24,
        right: 24,
        width: 56,
        height: 56,
        borderRadius: 28,
        backgroundColor: '#007AFF',
        justifyContent: 'center',
        alignItems: 'center',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 4,
        elevation: 8
    },
    fabText: {
        fontSize: 24,
        color: 'white',
        fontWeight: 'bold'
    }
});

export default NotesListScreen;