package com.example.notesapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.runtime.*
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.notesapp.data.NoteDatabase
import com.example.notesapp.data.NoteRepository
import com.example.notesapp.ui.*
import com.example.notesapp.ui.theme.NotesAppTheme

class MainActivity : ComponentActivity() {

    private lateinit var noteRepository: NoteRepository

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val database = NoteDatabase.getDatabase(this)
        noteRepository = NoteRepository(database.noteDao())

        setContent {
            NotesAppTheme {
                NotesApp(noteRepository)
            }
        }
    }
}

@Composable
fun NotesApp(noteRepository: NoteRepository) {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = "notes_list"
    ) {
        composable("notes_list") {
            val viewModel: NotesViewModel = viewModel(factory = NotesViewModelFactory(noteRepository))
            NotesScreen(
                viewModel = viewModel,
                onNoteClick = { noteId ->
                    navController.navigate("add_edit_note/$noteId")
                },
                onAddClick = {
                    navController.navigate("add_edit_note/-1")
                }
            )
        }

        composable("add_edit_note/{noteId}") { backStackEntry ->
            val noteId = backStackEntry.arguments?.getString("noteId")?.toInt() ?: -1
            val factory = EditNoteViewModelFactory(
                owner = backStackEntry,   // используем явное имя backStackEntry
                repository = noteRepository,
                noteId = noteId
            )
            val editViewModel: EditNoteViewModel = viewModel(
                key = "edit_note_$noteId",
                factory = factory
            )
            AddEditNoteScreen(
                viewModel = editViewModel,
                onNavigateBack = { navController.popBackStack() }
            )
        }
    }
}