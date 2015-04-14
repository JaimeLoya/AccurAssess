# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AccAssess
                                 A QGIS plugin
 Generate an error matrix and measures of mapping accuracy for raster anad vector layers.
                              -------------------
        begin                : 2014-02-19
        copyright            : (C) 2014 by Jaime Loya, Jean F Mas
        email                : jaimeloyac@gmail.com, jfmas@ciga.unam.mx
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.analysis import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from accassessdialog import AccAssessDialog
import os.path

# Import custom code that actually does stuff. All the other imports

from raster_handling import *
from error_matrix import *
import os,math,csv,sys

# Import numpy library
from numpy import *
class AccAssess:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
<<<<<<< HEAD
        localePath = os.path.join(self.plugin_dir, 'i18n', 'AccurAssess_{}.qm'.format(locale))
=======
        localePath = os.path.join(self.plugin_dir, 'i18n', 'accassess_{}.qm'.format(locale))
>>>>>>> 09a91b074571053f9f6f7c0a210fe32b983de012

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = AccAssessDialog()

    def initGui(self):
        # Create action that will start plugin configuration
<<<<<<< HEAD
        
        self.action = QAction(
            QIcon(":/plugins/AccurAssess/icon.png"),
=======
        self.action = QAction(
            QIcon(":/plugins/accassess/icon.png"),
>>>>>>> 09a91b074571053f9f6f7c0a210fe32b983de012
            u"AccurAssess", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
<<<<<<< HEAD
        
=======
        self.iface.addToolBarIcon(self.action)
>>>>>>> 09a91b074571053f9f6f7c0a210fe32b983de012
        self.iface.addPluginToMenu(u"&AccurAssess", self.action)
        
        # Hook the select button to a file dialog
        self.dlg.ui.outFileSelectButton.clicked.connect(self.showFileSelectDialog)
        
    def showFileSelectDialog(self):
        fname = QFileDialog.getSaveFileName(self.dlg, 'Save File', os.path.expanduser('~'))
        self.dlg.ui.outFileLineEdit.setText( fname )

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&AccurAssess", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
<<<<<<< HEAD
        cwd=os.getcwd()
        path=os.path.join(cwd,"icon.png")

=======
>>>>>>> 09a91b074571053f9f6f7c0a210fe32b983de012
        # populate the combo boxes with loaded layers
        self.dlg.initLayerCombobox( self.dlg.ui.referenceComboBox, 'key_of_default_layer' )
        self.dlg.initLayerCombobox( self.dlg.ui.comparisonComboBox, 'key_of_default_layer' )
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # This gets the layer label from the menu but that's not the key
        
        # get the  layer
        ref_layer= self.dlg.layerFromComboBox( self.dlg.ui.referenceComboBox )
        comp_layer=self.dlg.layerFromComboBox( self.dlg.ui.comparisonComboBox )
        # get the file name that's in the filename line edit (set in showFileSelectDialog)
        filename=str( self.dlg.ui.outFileLineEdit.text() )
        # See if OK was pressed
        if result == 1 and ref_layer.type()==QgsMapLayer.RasterLayer and comp_layer.type()==QgsMapLayer.RasterLayer:
            
            
            #Define a counter
            cont=1
            #While the counter is lower than 2, then repeats the structure of code
            while cont<=2:
                # get some RasterDS objects (defined in raster_handling.py) so we can do
                # gdal stuff.
                if cont==1:                
                    ref_ds = RasterDS(ref_layer)
                elif cont==2:
                    ref_ds = RasterDS(comp_layer)
                comp_ds = RasterDS(comp_layer)
                # get 2d arrays from datasets. I'm currently assuming the extents are 
                # the same. I'll need to change that later. I should also check the shape
                # of the band array.
                ref_arr = ref_ds.band_array[0]
                comp_arr = comp_ds.band_array[0]
                # I only want to compare non-zero values so I need the indexes of nonzeros
                idx = ref_arr.nonzero()
                # get the error matrix
                em = error_matrix(ref_arr[idx],comp_arr[idx])
              
                
                ###
                
                if cont==1:
                    filename1=filename+"_temp_matrix.csv"
                    em.save_csv( filename1 )
                elif cont==2:
                    filename2=filename+"_temp_area.csv"
                    em.save_csv( filename2 )
                # Increments the counter by ones                  
                cont+=1
            # Open the files obtained the Raw confusion matrix and the surfaces matrix
            csv_em=open(filename1)
            csv_sup=open(filename2)
            csv_matrix=open(filename+".csv",'wb')
            writer_csv=csv.writer(csv_matrix)
            
            # Set a list to save the elements for the raw matrix
            matrix_error=[]
            for rows_em in csv_em:
                row_em=rows_em.rstrip('\n')
                cell_mat=row_em.split(",")    
                matrix_error.append(cell_mat)
                
            # Set a list to save the elements for the matrix of surfaces      
            lis=[]
            for rows_sup in csv_sup:
                row_sup=rows_sup.rstrip('\n')
                lis_sup=row_sup.split(",")
                lis.append(lis_sup)
            sum_surfaces=sum(np.array(lis,dtype=int))
            # Set array of the length of total of classes
            adjusted_matrix=np.zeros((len(lis),len(lis)))
            
            # Set array of type float
            m_e=np.array(matrix_error,dtype=float)
            l_s=np.array(lis,dtype=float)

            # Set the size of the column
            col=(np.arange(len(lis))+1).reshape((len(lis),1))
            
            # set the title
            writer_csv.writerow([str(ref_layer.name())+" (Reference Map) versus "+str(comp_layer.name())+ " (Map Under Assessment)"])
            writer_csv.writerows([""])
            writer_csv.writerow(["Raw Matrix"])
            writer_csv.writerow(np.append("Map",np.arange(len(lis))+1))
            writer_csv.writerows(np.c_[col,matrix_error])
            writer_csv.writerows([""])
            
            # Set the adjust confusion matrix
            sup_tot=np.sum(l_s)
            for r_i in range(len(lis)):
                for r_j in range(len(lis)):
                    per_sup=np.sum(l_s[r_i])/sup_tot  
                    adjusted_matrix[r_i][r_j]=(m_e[r_i][r_j]*per_sup)/np.sum(m_e[r_i])
                  
            # Create a matrix for estimate the value, this will used for estimate the half-width CI of the user accuracy
            diagonal=np.diagonal(adjusted_matrix)
            mat_comp_1=np.zeros((len(lis),len(lis)))
            for x_i in range(len(lis)):
                for x_j in range(len(lis)):
                    per_sup2=np.sum(l_s[x_i])/sup_tot
                    mat_comp_1[x_i][x_j]=adjusted_matrix[x_i][x_j]*(per_sup2-adjusted_matrix[x_i][x_j])/np.sum(m_e[x_i])
            dia_comp_1=np.diagonal(mat_comp_1)
            
            user_accuracy=[]
            prod_accuracy=[]
            hci_user=[]
            hci_prod=[]
            for u_i in range(len(lis)):
                # Estimates user accuracy
                user_cal=(diagonal[u_i]/np.sum(adjusted_matrix[u_i]))    
                user_accuracy.append(user_cal)

                # Estimates producer accuracy
                prod_cal=(diagonal[u_i]/sum(adjusted_matrix,axis=0)[u_i])     
                prod_accuracy.append(prod_cal)

                # Estimates half CI user
                hci_u=1.96*math.sqrt((diagonal[u_i]*(np.sum(adjusted_matrix[u_i])-diagonal[u_i])/(np.sum(adjusted_matrix[u_i])*np.sum(adjusted_matrix[u_i])*np.sum(m_e[u_i]))))
                hci_user.append(hci_u)

                # Estimates half CI producer
<<<<<<< HEAD
                comp1=diagonal[u_i]*(np.sum(adjusted_matrix,axis=0)[u_i])**-4
                comp2=diagonal[u_i]*(sum(mat_comp_1,axis=0)[u_i]-dia_comp_1[u_i])
                comp3=(np.sum(adjusted_matrix[u_i])-diagonal[u_i])*(np.sum(adjusted_matrix,axis=0)[u_i]-diagonal[u_i])**2/sum(m_e,axis=1)[u_i]
                
                hci_p=1.96*math.sqrt(comp1*(comp2+comp3))
                hci_prod.append(hci_p)

=======
                comp1=diagonal[u_i]*(sum(mat_comp_1,axis=0)[u_i]-dia_comp_1[u_i])
                comp2=(((np.sum(adjusted_matrix[u_i])-diagonal[u_i]))*(np.sum(adjusted_matrix,axis=0)[u_i]-diagonal[u_i])**2)/sum(m_e,axis=1)[u_i]
                hci_p=1.96*math.sqrt((diagonal[u_i]*(np.sum(adjusted_matrix,axis=0)[u_i])**-4)*(comp1+comp2))
                hci_prod.append(hci_p)

            

>>>>>>> 09a91b074571053f9f6f7c0a210fe32b983de012
            ci_low_acc=[]
            ci_upp_acc=[]

            ci_low_prod=[]
            ci_upp_prod=[]

            # Estimates CI Lower Bound and CI Upper Bound for user and producer
            for low_up in range(len(lis)):
                cla_b=user_accuracy[low_up]-hci_user[low_up]
                cla=user_accuracy[low_up]+hci_user[low_up]

                clp_b=prod_accuracy[low_up]-hci_prod[low_up]
                clp=prod_accuracy[low_up]+hci_prod[low_up]
                if cla_b<0:cla_b=0
                if cla>1:cla=1

                if clp_b<0:clp_b=0
                if clp>1:clp=1
                
                ci_low_acc.append(cla_b)
                ci_upp_acc.append(cla)
                ci_low_prod.append(clp_b)
                ci_upp_prod.append(clp)
                
            
            
            adjusted_matrix_f=np.c_[col,adjusted_matrix]

            # Estimates HCI Overall accuracy
            hci_over_comp1=np.array(diagonal,dtype=float)*((np.sum(l_s,axis=1,dtype=float)/np.sum(l_s,dtype=float))-np.array(diagonal,dtype=float))/np.sum(m_e,axis=1,dtype=int)
            hci_overall=1.96*math.sqrt(sum(hci_over_comp1))

            # Save all indices in the csv file
            
            writer_csv.writerow(["Adjusted Confusion Matrix (Card Correction)"])
            writer_csv.writerow(np.append("Map",np.arange(len(lis))+1))
            writer_csv.writerows(adjusted_matrix_f)  
            writer_csv.writerows([""])
            writer_csv.writerow(np.append("Overall accuracy",[sum(diagonal)]))
            writer_csv.writerow(np.append("HCI Overall accuracy",[hci_overall]))
       
            writer_csv.writerows([""])
            writer_csv.writerow(np.append("Category",np.arange(len(lis))+1))  
            writer_csv.writerow(np.append("User Accuracy",user_accuracy))
            writer_csv.writerow(np.append("Half CI",hci_user))
            writer_csv.writerow(np.append("CI Lower Bound",ci_low_acc))
            writer_csv.writerow(np.append("CI Upper Bound",ci_upp_acc))
            writer_csv.writerow(np.append("Prod Accuracy",prod_accuracy))
            writer_csv.writerow(np.append("Half CI",hci_prod))
            writer_csv.writerow(np.append("CI Lower Bound",ci_low_prod))
            writer_csv.writerow(np.append("CI Upper Bound",ci_upp_prod))

            # Calculate proportion area and write in csv file        
            writer_csv.writerow (np.append("Error Adjusted-Proportion",(np.sum(adjusted_matrix,axis=0))))
            
            # Estiamte the Half-Widht confidence interval for the estimated area proportion
            
            transpose_sum=np.array(np.transpose(np.matrix(np.sum(m_e,axis=1,dtype=int))))
            mul_diag_mat=np.divide(adjusted_matrix*transpose_sum,m_e)
            hci_adjusted_area=(mul_diag_mat**2)*((m_e/transpose_sum)*(1-m_e/transpose_sum))/(transpose_sum-1)
    
            # Replace nan values with zeros 
            nans=isnan(hci_adjusted_area)
            hci_adjusted_area[nans]=0
            
            half_ci_area=np.array(np.sum(hci_adjusted_area,axis=0))
            half_ci_class=[]
            
            
            for hci_area in half_ci_area:
                elemen_hci=1.96*float(hci_area)**.5
                half_ci_class.append (format(elemen_hci,'.10f'))
                
            # Indices Half CI, CI Lower and Upper Bound for the proportion area    
            ci_low_area=np.sum(adjusted_matrix,axis=0)- np.array(half_ci_class,dtype=float)
            ci_up_area=np.sum(adjusted_matrix,axis=0)+ np.array(half_ci_class,dtype=float)

            # Round CI Lower value if is less than zero or CI Upper value if is greater than one 
            for i_area in range(len(ci_low_area)):
                if ci_low_area[i_area]<0: ci_low_area[i_area]=0
                if ci_up_area[i_area]>1: ci_up_area[i_area]=1
                

            #  Stored the Half CI and CI Lower and Upper indices
            writer_csv.writerow(np.append("Half CI",half_ci_class))
            writer_csv.writerow(np.append("CI Lower Bound",ci_low_area))
            writer_csv.writerow(np.append("CI Upper Bound",ci_up_area))
            # Close all files CSV that were opened
            csv_matrix.close()
            csv_em.close()
            csv_sup.close()
            os.remove(filename1)
            os.remove(filename2)
<<<<<<< HEAD
=======
            
            # Show a finished message
>>>>>>> 09a91b074571053f9f6f7c0a210fe32b983de012
            QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('AccurAssess', "Finished"), QCoreApplication.translate('AccurAssess', "Operation completed successfully"))
        elif result == 1 and ref_layer.type()==QgsMapLayer.VectorLayer and comp_layer.type()==QgsMapLayer.VectorLayer:
            # Creates a CSV file to save all indices
            csv_matrix=open(filename+".csv",'wb')
            writer_csv=csv.writer(csv_matrix)
            
<<<<<<< HEAD
    
=======
            
            # Calculates the area from each features in comparison layer
            
            areabypolygon=[]
            clave_area=[]
            for f in comp_layer.getFeatures():
                clave_area.append(f[0])
                area_polygon=f.geometry().area()
                areabypolygon.append(f[0])
                areabypolygon.append(area_polygon)
           
>>>>>>> 09a91b074571053f9f6f7c0a210fe32b983de012
            
            # Make a intersect feature
            split_filename=filename.split(".")
            overlayAnalyzer=QgsOverlayAnalyzer()
            intersect=overlayAnalyzer.intersection(ref_layer,comp_layer,filename+".shp")
            
            # Add layer to the table of contents
            layer_inter=QgsVectorLayer(filename+".shp","intersect","ogr")
            add_inter=QgsMapLayerRegistry.instance().addMapLayer(layer_inter)

          
<<<<<<< HEAD
            # This stored in separate lists, each value in the intersect layer
=======
            # This stored in separate lists, each value in the layer
>>>>>>> 09a91b074571053f9f6f7c0a210fe32b983de012
            clave1=[]
            clave2=[]
            area_values=[]
            for reg in add_inter.getFeatures():
               
                try:
                    a=int(reg[0])
                    b=int(reg[1])
                    clave1.append(str(a)+"_"+str(b))
                    clave2.append(b)
                    area_values.append(str(b))
                    area_values.append(reg[2])
                except:
                    pass
            unique_value=list(set(clave1))
            unique_class=list(set(clave2))
            # Set the size of the matrix 
            matrix=np.zeros((len(unique_class),len(unique_class)))
            
            # Makes the summary table by class
<<<<<<< HEAD

            claves=[]
            sumas=[]
            for f in comp_layer.getFeatures():
                    if (f[0] in claves)==False:
                            claves.append(f[0])
                            sumas.append(f.geometry().area())
                            
                    elif (f[0] in claves)==True:
                            index=claves.index(f[0])
                            sumas[index]=sumas[index]+f.geometry().area()
                                      
            lista=[]
            for j in range(len(claves)):
                    lista.append([claves[j],sumas[j]])

            lista.sort()

            sum_areas=[]
            for l in range(len(lista)):
                    sum_areas.append(lista[l][1])
=======
            sum_areas=[]
            suma_shp=0
            c=0
            d=1
            for m in range(len(unique_class)):
                for n in range (len(areabypolygon)):
                    try:
                        val_area=int(areabypolygon[c])
                        if val_area==unique_class[m]:
                            suma_shp=suma_shp+float(areabypolygon[d])
                    except:
                        pass
                    c=c+2
                    d=d+2
                c=0
                d=1
                sum_areas.append(suma_shp)
                suma_shp=0
>>>>>>> 09a91b074571053f9f6f7c0a210fe32b983de012
                
            # Estimates the proportion area by class
            proportion_area=np.array(sum_areas)/np.sum(sum_areas)
           
            # Estimates the total points by class
            for x in range(len(unique_value)):
                
                tot_point_cve=clave1.count(unique_value[x])
                split_unique=unique_value[x].split("_")
                matrix[int(split_unique[1])-1,int(split_unique[0])-1]=tot_point_cve
            matrix_points=np.array(matrix)
            adjusted_matrix=matrix
            
            # Set the title and stores the raw matrix
            writer_csv.writerow([str(ref_layer.name())+" (Reference Map) versus "+str(comp_layer.name())+ " (Map Under Assessment)"])
            writer_csv.writerows([""])
            writer_csv.writerow(["Raw Matrix"])
            writer_csv.writerow(np.append("Map",np.arange(len(unique_class))+1))
            writer_csv.writerows(np.c_[unique_class,adjusted_matrix])
            writer_csv.writerows([""])
          
            # Estimates total points by column and row
            tot_points_col=[]
            tot_points_row=[]
            for sum_rc in range(len(unique_class)):
                point_col=np.sum(adjusted_matrix[sum_rc])
                tot_points_col.append(point_col)
                point_row=np.sum(adjusted_matrix,axis=0)[sum_rc]
                tot_points_row.append(point_row)
                
            # Set adjust matrix
            for col in range(len(unique_class)):
                for row in range (len(unique_class)):
                    if adjusted_matrix[col][row]!=0:
                        adjusted_matrix[col][row]=(adjusted_matrix[col][row]*proportion_area[col])/tot_points_col[col]
         
            # Determines the diagonal of the matrix
            diagonal_shp=np.diagonal(adjusted_matrix)

            matr_comp=np.zeros((len(unique_class),len(unique_class)))
            # Matrix to half-ci
            for col2 in range(len(unique_class)):
                for row2 in range(len(unique_class)):
                    matr_comp[col2][row2]=(adjusted_matrix[col2][row2]*(proportion_area[col2]-adjusted_matrix[col2][row2]))/tot_points_col[col2]
            dia_comp_1=np.diagonal(matr_comp)
            # Makes lists to save user accuracy, producer accuracy, hci user and hci producer 
            user_accuracy=[]
            prod_accuracy=[]
            hci_user=[]
            hci_prod=[]
            for indice in range(len(unique_class)):
                # Calculate user accuracy
                user_cal=(diagonal_shp[indice]/np.sum(adjusted_matrix[indice]))
                user_accuracy.append(user_cal)
                
                # Calculate producer accuracy
                prod_cal=(diagonal_shp[indice]/np.sum(adjusted_matrix,axis=0)[indice])
                prod_accuracy.append(prod_cal)

                # Calculate half CI user
                hci_u=1.96*math.sqrt((diagonal_shp[indice]*(np.sum(adjusted_matrix[indice])-diagonal_shp[indice])/(np.sum(adjusted_matrix[indice])*np.sum(adjusted_matrix[indice])*tot_points_col[indice])))
                hci_user.append(hci_u)

                # Calculate half CI producer
<<<<<<< HEAD
                comp1=diagonal_shp[indice]*(np.sum(adjusted_matrix,axis=0)[indice])**-4
                comp2=diagonal_shp[indice]*(np.sum(matr_comp,axis=0)[indice]-dia_comp_1[indice])
                comp3=(((np.sum(adjusted_matrix[indice])-diagonal_shp[indice]))*(np.sum(adjusted_matrix,axis=0)[indice]-diagonal_shp[indice])**2)/sum(matrix_points,axis=1)[indice]
                hci_p=1.96*math.sqrt(comp1*(comp2+comp3))
                hci_prod.append(hci_p)

=======
                comp1=diagonal_shp[indice]*(np.sum(matr_comp,axis=0)[indice]-dia_comp_1[indice])
                comp2=(((np.sum(adjusted_matrix[indice])-diagonal_shp[indice]))*(np.sum(adjusted_matrix,axis=0)[indice]-diagonal_shp[indice])**2)/sum(matrix_points,axis=1)[indice]
                hci_p=1.96*math.sqrt((diagonal_shp[indice]*(np.sum(adjusted_matrix,axis=0)[indice])**-4)*(comp1+comp2))
                hci_prod.append(hci_p)
           
          
>>>>>>> 09a91b074571053f9f6f7c0a210fe32b983de012
            
            ci_low_acc=[]
            ci_upp_acc=[]

            ci_low_prod=[]
            ci_upp_prod=[]

            # Calculate CI Lower Bound and CI Upper Bound for user an producer
            for low_up in range (len(unique_class)):
                cla_b=user_accuracy[low_up]-hci_user[low_up]
                cla=user_accuracy[low_up]+hci_user[low_up]

                clp_b=prod_accuracy[low_up]-hci_prod[low_up]
                clp=prod_accuracy[low_up]+hci_prod[low_up]

                if cla_b<0:cla_b=0
                if cla>1:cla=1

                if clp_b<0:clp_b=0
                if clp>1:clp=1
                
                ci_low_acc.append(cla_b)
                ci_upp_acc.append(cla)
                ci_low_prod.append(clp_b)
                ci_upp_prod.append(clp)

            # Determines the appropriate headers to each class
            columns=(np.arange(len(unique_class))+1).reshape((len(unique_class),1))
            adjusted_matrix_f=np.c_[columns,adjusted_matrix]
           
            # Estimates HCI Overall accuracy
            hci_over_comp1=np.array(diagonal_shp,dtype=float)*(proportion_area-np.array(diagonal_shp,dtype=float))/np.sum(matrix_points,axis=1,dtype=int)
            hci_overall=1.96*math.sqrt(sum(hci_over_comp1))
            
            # Save all indices in CSV file
            writer_csv.writerow(["Adjusted Confusion Matrix (Card Correction)"])
            writer_csv.writerow(np.append("Map",np.arange(len(unique_class))+1))    
            writer_csv.writerows(adjusted_matrix_f)
            
            writer_csv.writerows([""])
            writer_csv.writerow(np.append("Overall Accuracy",[sum(diagonal_shp)]))
            writer_csv.writerow(np.append("HCI Overall Accuracy",hci_overall))
            writer_csv.writerows([""])
            writer_csv.writerow(np.append("Category",np.arange(len(unique_class))+1))  
            writer_csv.writerow(np.append("User Accuracy",user_accuracy))
            writer_csv.writerow(np.append("Half CI",hci_user))
            writer_csv.writerow(np.append("CI Lower Bound",ci_low_acc))
            writer_csv.writerow(np.append("CI Upper Bound",ci_upp_acc))
            writer_csv.writerow(np.append("Prod Accuracy",prod_accuracy))
            writer_csv.writerow(np.append("Half CI",hci_prod))
            writer_csv.writerow(np.append("CI Lower Bound",ci_low_prod))
            writer_csv.writerow(np.append("CI Upper Bound",ci_upp_prod))
          
            # Calculate proportion area and write in csv file        
            writer_csv.writerow (np.append("Error Adjusted-Proportion",(np.sum(matrix,axis=0))))
            # Estiamte the Half-Widht confidence interval for the estimated area proportion
            transpose_sum=np.array(np.transpose(np.matrix(np.sum(matrix_points,axis=1,dtype=int))))
            mul_diag_mat=np.divide(adjusted_matrix*transpose_sum,matrix_points)
            hci_adjusted_area=(mul_diag_mat**2)*((matrix_points/transpose_sum)*(1-matrix_points/transpose_sum))/(transpose_sum-1)
          
            # Replace nan values with zeros 
            nans=isnan(hci_adjusted_area)
            hci_adjusted_area[nans]=0
            
            half_ci_area=np.array(np.sum(hci_adjusted_area,axis=0))
            half_ci_class=[]
            
            for hci_area in half_ci_area:
                elemen_hci=1.96*float(hci_area)**.5
                half_ci_class.append (format(elemen_hci,'.10f'))
                
            # Indices Half CI, CI Lower and Upper Bound for the proportion area    
            ci_low_area=np.sum(matrix,axis=0)- np.array(half_ci_class,dtype=float)
            ci_up_area=np.sum(matrix,axis=0)+ np.array(half_ci_class,dtype=float)

            # Round CI Lower value if is less than zero or CI Upper value if is greater than one 
            for i_area in range(len(ci_low_area)):
                if ci_low_area[i_area]<0: ci_low_area[i_area]=0
                if ci_up_area[i_area]>1: ci_up_area[i_area]=1
                

            #  Stored the Half and CI indices
            writer_csv.writerow(np.append("Half CI",half_ci_class))
            writer_csv.writerow(np.append("CI Lower Bound",ci_low_area))
            writer_csv.writerow(np.append("CI Upper Bound",ci_up_area))

            # Close CSV file
            csv_matrix.close()
            # Remove from table of contents the intersect layer
            remove_layer=QgsMapLayerRegistry.instance().removeMapLayer(layer_inter.id())
            # Delete temporal files
            temp_files=[".dbf",".prj",".qpj",".shp",".shx"]
            for temp_file in temp_files:
                os.remove(filename+temp_file)
<<<<<<< HEAD
=======
            # Show a finished message
>>>>>>> 09a91b074571053f9f6f7c0a210fe32b983de012
            QMessageBox.information(self.iface.mainWindow(), QCoreApplication.translate('AccurAssess', "Finished"), QCoreApplication.translate('AccurAssess', "Operation completed successfully"))
        # Displays an error message if the parameters are incorrect
        elif result == 1 and filename=="":
            QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('Error', "Error"), QCoreApplication.translate('Error', "Error try again, make sure of give all parameters"))
        elif result == 1 and ref_layer.type()==QgsMapLayer.VectorLayer and comp_layer.type()==QgsMapLayer.RasterLayer:
            QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('Error', "Error"), QCoreApplication.translate('Error', "Error try again, please, make sure of use two raster files or two shapefiles."))
        elif result == 1 and ref_layer.type()==QgsMapLayer.RasterLayer and comp_layer.type()==QgsMapLayer.VectorLayer:
            QMessageBox.critical(self.iface.mainWindow(), QCoreApplication.translate('Error', "Error"), QCoreApplication.translate('Error', "Error try again, please, make sure of use two raster files or two shapefiles."))   
        else:
            pass
            
        
