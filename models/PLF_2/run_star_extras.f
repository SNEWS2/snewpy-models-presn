! ***********************************************************************
!
!   Copyright (C) 2010  Bill Paxton
!
!   this file is part of mesa.
!
!   mesa is free software; you can redistribute it and/or modify
!   it under the terms of the gnu general library public license as published
!   by the free software foundation; either version 2 of the license, or
!   (at your option) any later version.
!
!   mesa is distributed in the hope that it will be useful, 
!   but without any warranty; without even the implied warranty of
!   merchantability or fitness for a particular purpose.  see the
!   gnu library general public license for more details.
!
!   you should have received a copy of the gnu library general public license
!   along with this software; if not, write to the free software
!   foundation, inc., 59 temple place, suite 330, boston, ma 02111-1307 usa
!
! ***********************************************************************
 
      module run_star_extras

      use star_lib
      use star_def
      use const_def
      
      implicit none
      
      ! these routines are called by the standard run_star check_model
      contains
      
      subroutine extras_controls(id, ierr)
         integer, intent(in) :: id
         integer, intent(out) :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         
         ! this is the place to set any procedure pointers you want to change
         ! e.g., other_wind, other_mixing, other_energy  (see star_data.inc)
         
         
      end subroutine extras_controls
      
      
      integer function extras_startup(id, restart, ierr)
         integer, intent(in) :: id
         logical, intent(in) :: restart
         integer, intent(out) :: ierr
         logical :: set
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         extras_startup = 0
         if (.not. restart) then
            call alloc_extra_info(s)
         else ! it is a restart
            call unpack_extra_info(s)
         end if
         
         !When to switch resolution 
         !extras_ipar(1)
         !When to switch off thermohaline
         !extras_ipar(2)
         !Number:
         !0 Never
         !1 He_core_mass>0
         !2 c_core_mass>0
         !3 o_core_mass >0
         !4 si_core_mass>0
         !5 fe_core_mass>0
         
         
         !New convergencee settings
         !extras_rpar(1) dX_nuc_drop_limit = 5d-2
         !extras_rpar(2) dX_nuc_drop_limit_at_high_T = 5d-3
         !extras_rpar(3) dX_nuc_drop_min_X_limit = 5d-2
         
         set=.FALSE.
         SELECT CASE(s%job%extras_ipar(1))
         CASE(1)
				IF(s%he_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(2)
				IF(s%c_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(3)
				IF(s%o_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(4)
				IF(s%si_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(5)
				IF(s%fe_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE DEFAULT
				set=.FALSE.
         END SELECT
				
         if(set) THEN
				s%dX_nuc_drop_limit=s%job%extras_rpar(1)
				s%dX_nuc_drop_limit_at_high_T=s%job%extras_rpar(2)
				s%dX_nuc_drop_min_X_limit=s%job%extras_rpar(3)
         end if
				
			
         set=.FALSE.
         SELECT CASE(s%job%extras_ipar(2))
         CASE(1)
				IF(s%he_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(2)
				IF(s%c_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(3)
				IF(s%o_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(4)
				IF(s%si_core_mass>0.d0)THEN
					set=.TRUE.
         		END IF
         CASE(5)
				IF(s%fe_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE DEFAULT
				set=.FALSE.
         END SELECT
				
         if(set) THEN
				s%thermohaline_coeff = 0.0
         end if
				 

	      s%max_dq=s%job%extras_rpar(4)/s%star_mass         
         
      end function extras_startup
      

      ! returns either keep_going, retry, backup, or terminate.
      integer function extras_check_model(id, id_extra)
         integer, intent(in) :: id, id_extra
         integer :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         
         
      end function extras_check_model


      integer function how_many_extra_history_columns(id, id_extra)
         integer, intent(in) :: id, id_extra
         integer :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         how_many_extra_history_columns = 0
      end function how_many_extra_history_columns
      
      
      subroutine data_for_extra_history_columns(id, id_extra, n, names, vals, ierr)
         integer, intent(in) :: id, id_extra, n
         character (len=maxlen_history_column_name) :: names(n)
         real(dp) :: vals(n)
         integer, intent(out) :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         
         !note: do NOT add the extras names to history_columns.list
         ! the history_columns.list is only for the built-in log column options.
         ! it must not include the new column names you are adding here.
         

      end subroutine data_for_extra_history_columns

      
      integer function how_many_extra_profile_columns(id, id_extra)
         use star_def, only: star_info
         integer, intent(in) :: id, id_extra
         integer :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         how_many_extra_profile_columns = 0
      end function how_many_extra_profile_columns
      
      
      subroutine data_for_extra_profile_columns(id, id_extra, n, nz, names, vals, ierr)
         use star_def, only: star_info, maxlen_profile_column_name
         use const_def, only: dp
         integer, intent(in) :: id, id_extra, n, nz
         character (len=maxlen_profile_column_name) :: names(n)
         real(dp) :: vals(nz,n)
         integer, intent(out) :: ierr
         type (star_info), pointer :: s
         integer :: k
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         
         !note: do NOT add the extra names to profile_columns.list
         ! the profile_columns.list is only for the built-in profile column options.
         ! it must not include the new column names you are adding here.

         ! here is an example for adding a profile column
         !if (n /= 1) stop 'data_for_extra_profile_columns'
         !names(1) = 'beta'
         !do k = 1, nz
         !   vals(k,1) = s% Pgas(k)/s% P(k)
         !end do
         
      end subroutine data_for_extra_profile_columns
      

      ! returns either keep_going or terminate.
      ! note: cannot request retry or backup; extras_check_model can do that.
      integer function extras_finish_step(id, id_extra)
         integer, intent(in) :: id, id_extra
         integer :: ierr
         logical :: set
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         extras_finish_step = keep_going


         
         !When to switch resolution 
         !extras_ipar(1)
         !When to switch off thermohaline
         !extras_ipar(2)
         !Number:
         !0 Never
         !1 He_core_mass>0
         !2 c_core_mass>0
         !3 o_core_mass >0
         !4 si_core_mass>0
         !5 fe_core_mass>0
         
         
         !New convergencee settings
         !extras_rpar(1) dX_nuc_drop_limit = 5d-2
         !extras_rpar(2) dX_nuc_drop_limit_at_high_T = 5d-3
         !extras_rpar(3) dX_nuc_drop_min_X_limit = 5d-2
         
         set=.FALSE.
         SELECT CASE(s%job%extras_ipar(1))
         CASE(1)
				IF(s%he_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(2)
				IF(s%c_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(3)
				IF(s%o_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(4)
				IF(s%si_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(5)
				IF(s%fe_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE DEFAULT
				set=.FALSE.
         END SELECT
				
         if(set) THEN
				s%dX_nuc_drop_limit=s%job%extras_rpar(1)
				s%dX_nuc_drop_limit_at_high_T=s%job%extras_rpar(2)
				s%dX_nuc_drop_min_X_limit=s%job%extras_rpar(3)
         end if
				
			
         set=.FALSE.
         SELECT CASE(s%job%extras_ipar(2))
         CASE(1)
				IF(s%he_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(2)
				IF(s%c_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(3)
				IF(s%o_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE(4)
				IF(s%si_core_mass>0.d0)THEN
					set=.TRUE.
         		END IF
         CASE(5)
				IF(s%fe_core_mass>0.d0)THEN
					set=.TRUE.
				END IF
         CASE DEFAULT
				set=.FALSE.
         END SELECT
				
         if(set) THEN
				s%thermohaline_coeff = 0.0
         end if
				

	      s%max_dq=s%job%extras_rpar(4)/s%star_mass

      end function extras_finish_step
      
      
      subroutine extras_after_evolve(id, id_extra, ierr)
         integer, intent(in) :: id, id_extra
         integer, intent(out) :: ierr
         type (star_info), pointer :: s
         ierr = 0
         call star_ptr(id, s, ierr)
         if (ierr /= 0) return
         
			
      end subroutine extras_after_evolve
      
      
      ! routines for saving and restoring extra data so can do restarts
         
         ! put these defs at the top and delete from the following routines
         !integer, parameter :: extra_info_alloc = 1
         !integer, parameter :: extra_info_get = 2
         !integer, parameter :: extra_info_put = 3
      
      
      subroutine alloc_extra_info(s)
         integer, parameter :: extra_info_alloc = 1
         type (star_info), pointer :: s
         call move_extra_info(s,extra_info_alloc)
      end subroutine alloc_extra_info
      
      
      subroutine unpack_extra_info(s)
         integer, parameter :: extra_info_get = 2
         type (star_info), pointer :: s
         call move_extra_info(s,extra_info_get)
      end subroutine unpack_extra_info
      
      
      subroutine store_extra_info(s)
         integer, parameter :: extra_info_put = 3
         type (star_info), pointer :: s
         call move_extra_info(s,extra_info_put)
      end subroutine store_extra_info
      
      
      subroutine move_extra_info(s,op)
         integer, parameter :: extra_info_alloc = 1
         integer, parameter :: extra_info_get = 2
         integer, parameter :: extra_info_put = 3
         type (star_info), pointer :: s
         integer, intent(in) :: op
         
         integer :: i, j, num_ints, num_dbls, ierr
         
         i = 0
         ! call move_int or move_flg    
         num_ints = i
         
         i = 0
         ! call move_dbl       
         
         num_dbls = i
         
         if (op /= extra_info_alloc) return
         if (num_ints == 0 .and. num_dbls == 0) return
         
         ierr = 0
         call star_alloc_extras(s% id, num_ints, num_dbls, ierr)
         if (ierr /= 0) then
            write(*,*) 'failed in star_alloc_extras'
            write(*,*) 'alloc_extras num_ints', num_ints
            write(*,*) 'alloc_extras num_dbls', num_dbls
            stop 1
         end if
         
         contains
         
         subroutine move_dbl(dbl)
            real(dp) :: dbl
            i = i+1
            select case (op)
            case (extra_info_get)
               dbl = s% extra_work(i)
            case (extra_info_put)
               s% extra_work(i) = dbl
            end select
         end subroutine move_dbl
         
         subroutine move_int(int)
            integer :: int
            i = i+1
            select case (op)
            case (extra_info_get)
               int = s% extra_iwork(i)
            case (extra_info_put)
               s% extra_iwork(i) = int
            end select
         end subroutine move_int
         
         subroutine move_flg(flg)
            logical :: flg
            i = i+1
            select case (op)
            case (extra_info_get)
               flg = (s% extra_iwork(i) /= 0)
            case (extra_info_put)
               if (flg) then
                  s% extra_iwork(i) = 1
               else
                  s% extra_iwork(i) = 0
               end if
            end select
         end subroutine move_flg
      
      end subroutine move_extra_info


      end module run_star_extras
      

