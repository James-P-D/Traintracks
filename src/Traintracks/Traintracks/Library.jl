CELL_EMPTY = 0
CELL_HORIZONTAL = 1
CELL_VERTICAL = 2
CELL_TOP_LEFT = 3
CELL_TOP_RIGHT = 4
CELL_BOTTOM_RIGHT = 5
CELL_BOTTOM_LEFT = 6
TOTAL_CELL_STATES = 7

function check_cells(cell_cols, cell_rows, col1, row1, col2, row2, visited_grid)
    next_cells = []
    
    if ((col1 > 0) && (col1 <= cell_cols) && (row1 > 0) && (row1 <= cell_rows) && (!visited_grid[col1, row1]))
        push!(next_cells, (col1, row1))        
    end
    if ((col2 > 0) && (col2 <= cell_cols) && (row2 > 0) && (row2 <= cell_rows) && (!visited_grid[col2, row2]))
        if (!(visited_grid[col2, row2]))
            push!(next_cells, (col2, row2))
        end
    end
    return next_cells            
end

function get_next_cell(cell_cols, cell_rows, col, row, visited_grid, grid)
    state = grid[col, row]
    if (state == CELL_HORIZONTAL)
        return check_cells(cell_cols, cell_rows, col + 1, row, col - 1, row, visited_grid)
    elseif (state == CELL_VERTICAL)
        return check_cells(cell_cols, cell_rows, col, row - 1, col, row + 1, visited_grid)
    elseif (state == CELL_TOP_LEFT)
        return check_cells(cell_cols, cell_rows, col, row - 1, col - 1, row, visited_grid)
    elseif (state == CELL_TOP_RIGHT)
        return check_cells(cell_cols, cell_rows, col, row - 1, col + 1, row, visited_grid)
    elseif (state == CELL_BOTTOM_RIGHT)
        return check_cells(cell_cols, cell_rows, col, row + 1, col + 1, row, visited_grid)
    elseif (state == CELL_BOTTOM_LEFT)
        return check_cells(cell_cols, cell_rows, col, row + 1, col - 1, row, visited_grid)
    end
    return next_cells
end

function is_complete(cell_cols, cell_rows, top_numbers, right_numbers, start_terminal, end_terminal, grid)
    println("is_complete()!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
	for col = 1:cell_cols    
		println("checking col ", col)

		total = 0
	    for row = 1:cell_rows
			if (grid[col, row] != CELL_EMPTY)
				total += 1
			end
		end 
		if (top_numbers[col] != total)
			println("fail expected ", top_numbers[col], " but got ", total)
			return false
		end
    end

	for row = 1:cell_rows
		println("checking row ", row)
		total = 0
	    for col = 1:cell_cols
			if (grid[col, row] != CELL_EMPTY)
				total += 1
			end
		end 
		if (right_numbers[row] != total)
			println("fail expected ", right_numbers[row], " but got ", total)
			return false
		end
    end

    # Create an array cell_cols-by-cell_rows in size, initialised to false
    visited_grid = fill(false, cell_cols, cell_rows)

    (start_terminal_col, start_terminal_row) = start_terminal
    (end_terminal_col, end_terminal_row) = end_terminal
    current_col = start_terminal_col + 1
    current_row = start_terminal_row + 1
    end_col = end_terminal_col + 1
    end_row = end_terminal_row + 1
    
    while ((current_col != end_col) && (current_row != end_row))
        visited_grid[current_col, current_row] = true
        
        next_cells = get_next_cell(cell_cols, cell_rows, current_col, current_row, visited_grid, grid)

        if (length(next_cells) != 1)
            return false
        end
        
        (current_col, current_row) = next_cells[1]
    end

	return true
end

function get_possible_states(current_col, current_row, next_col, next_row, grid)
    println("get_possible_states")
    println("current_col = ", current_col)
    println("current_row = ", current_row)
    println("next_col = ", next_col)
    println("next_row = ", next_row)
        
    current_cell_state = grid[current_col, current_row]
    if (current_col == next_col)
        if (next_row < current_row)
            return [CELL_VERTICAL, CELL_BOTTOM_LEFT, CELL_BOTTOM_RIGHT]
        elseif (next_row > current_row)
            return [CELL_VERTICAL, CELL_TOP_LEFT, CELL_TOP_RIGHT]
        else
            throw(DomainError(0, "something went wrong 1!"))
        end
    elseif (current_row == next_row)
        if (next_col < current_col)
            return [CELL_HORIZONTAL, CELL_TOP_RIGHT, CELL_BOTTOM_RIGHT]
        elseif (next_col > current_col)
            return [CELL_HORIZONTAL, CELL_BOTTOM_LEFT, CELL_TOP_LEFT]
        else
            throw(DomainError(0, "something went wrong 2!"))
        end
    else
        throw(DomainError(0, "something went wrong 3!"))
    end
end

function draw_grid(cell_cols, cell_rows, grid)
    println("+--------+")
    for row = 1:cell_rows
        print("|")
        for col = 1:cell_cols
            if(grid[col,row]==CELL_EMPTY)
                print(" ")
            else
                print(grid[col,row])
            end
		end
        println("|")
    end
    println("+--------+")
end

function sub_solve(cell_cols, cell_rows, top_numbers, right_numbers, current_col, current_row, end_col, end_row, visited_grid, start_terminal, end_terminal, grid, moves)
    println("sub_solve")
    println("current_col = ", current_col)
    println("current_row = ", current_row)
    draw_grid(cell_cols, cell_rows, grid)
    
    if ((current_col == end_col) && (current_row == end_row))
        if (is_complete(cell_cols, cell_rows, top_numbers, right_numbers, start_terminal, end_terminal, grid))
            return (true, moves)
        else
            return (false, moves)
        end
    else
        visited_grid[current_col, current_row] = true   
        next_cells = get_next_cell(cell_cols, cell_rows, current_col, current_row, visited_grid, grid)

        if (length(next_cells) != 1)
            return (false, [])
        else
            (next_col, next_row) = next_cells[1]
            println("next_col = ", next_col)
            println("next_row = ", next_row)
            
            if (grid[next_col, next_row] != CELL_EMPTY)
                println("Already at a permanent cell!")
                return sub_solve(cell_cols, cell_rows, top_numbers, right_numbers, next_col, next_row, end_col, end_row, visited_grid, start_terminal, end_terminal, grid, moves)
            else
                possible_states = get_possible_states(current_col, current_row, next_col, next_row, grid)
                for possible_state in possible_states
                    println("possible_state = ", possible_state)
                    grid[next_col, next_row] = possible_state
                    (successful, new_moves) = sub_solve(cell_cols, cell_rows, top_numbers, right_numbers, next_col, next_row, end_col, end_row, visited_grid, start_terminal, end_terminal, grid, moves)
                    if (successful)
                        println("possible_state = ", possible_state, " worked!")
                        return (true, [])
                    else
                        println("possible_state = ", possible_state, " failed")
                        grid[next_col, next_row] = CELL_EMPTY
                    end
                end
                return (false, moves)
            end            
        end
    end
end

function solve(cell_cols, cell_rows, top_numbers, right_numbers, start_terminal, end_terminal, grid)
    println("solve")
    (start_col, start_row) = start_terminal
    (end_col, end_row) = end_terminal
    
    # Create an array cell_cols-by-cell_rows in size, initialised to false
    visited_grid = fill(false, cell_cols, cell_rows)
         
    return sub_solve(cell_cols, cell_rows, top_numbers, right_numbers, start_col + 1, start_row + 1, end_col + 1, end_row + 1, visited_grid, start_terminal, end_terminal, grid, [])
end